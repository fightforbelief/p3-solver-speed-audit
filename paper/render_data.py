"""Render manuscript tables and interval plot from the archived result tables."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

PAPER = Path(__file__).resolve().parent
RESULTS = PAPER.parent / "results"


def read(name):
    with (RESULTS / name).open(newline="") as f:
        return list(csv.DictReader(f))


def table(path, headings, rows):
    lines = ["#table(columns: "+str(len(headings))+",",
             "align: (left, "+", ".join(["right"]*(len(headings)-1))+"),",
             "stroke: none, inset: (x: 4pt, y: 3pt),",
             "table.hline(),", "table.header("+",".join("[*"+v+"*]" for v in headings)+"),", "table.hline(stroke: 0.4pt),"]
    for row in rows:
        lines.append(",".join("["+str(v)+"]" for v in row)+",")
    lines.extend(["table.hline(),",")"])
    (PAPER/path).write_text("\n".join(lines)+"\n")


def main():
    replay = read("replays.csv")
    primary = [r for r in replay if r["slice_pct"] == "1"]
    audits = {(r["scenario"],int(r["budget_pct"]),r["design"]):r for r in read("audits.csv") if r["slice_pct"]=="1"}
    meta = {r["scenario"]:r for r in read("datasets.csv")}
    cap = [r for r in read("capped.csv") if r["slice_pct"]=="1"]
    rows, width_rows, cap_rows = [], [], []
    fig, ax = plt.subplots(figsize=(6.55,3.1), layout="constrained")
    for i, row in enumerate(primary):
        s = row["scenario"]
        stats = [audits[s,b,"minimax"] for b in (0,10,25)]
        indep, paired = (float(row[x]) for x in ("independence_ratio","paired_ratio"))
        rows.append([s, meta[s]["test"], row["n"], row["failures"],f"{indep:.3f}",f"{paired:.4f}"])
        for shift, col, d in zip((.18,0,-.18), ("#9ba7b1","#007084","#af4d25"), stats):
            lo,hi = float(d["lower"]),float(d["upper"])
            ax.plot([lo,hi],[i+shift]*2,color=col,linewidth=2.4,solid_capstyle="butt")
        ax.scatter(paired,i,marker="o",s=18,color="#171f25",zorder=4)
        ax.scatter(indep,i,marker="x",s=26,linewidths=1.2,color="#455366",zorder=4)
        u=audits[s,10,"uniform"]
        w=stats[1]
        width_rows.append([s,w["q"],f'{float(stats[0]["worst_width"]):.3f}',
                           f'{float(w["worst_width"]):.3f}', f'{float(u["worst_width"]):.3f}',
                           f'{float(w["lower"]):.3f}–{float(w["upper"]):.3f}'])
    for r in cap:
        s=r["scenario"]
        by_slice=[float(x["paired_ratio"]) for x in replay if x["scenario"]==s]
        cap_rows.append([s, f"{by_slice[1]:.3f}", f"{by_slice[2]:.3f}",f'{float(r["actual"]):.3f}',
                         r["reference_solved"],r["schedule_solved"]])
    ax.axvline(1,color="#686868",linestyle="--",linewidth=.8,zorder=0)
    ax.set_yticks(range(len(primary)),[r["scenario"] for r in primary])
    ax.invert_yaxis()
    ax.set_xlabel("Schedule time / reference time")
    ax.spines[["top","right","left"]].set_visible(False)
    ax.tick_params(axis="y",length=0)
    handles=[Line2D([0],[0],color=c,lw=2.4,label=l) for c,l in zip(("#9ba7b1","#007084","#af4d25"),("No checks","10% checked","25% checked"))]
    handles += [Line2D([0],[0],ls="",marker=m,color="#27323a",label=l,markersize=4) for m,l in [("o","Fully paired"),("x","Uniform pairing")]]
    ax.legend(handles=handles,loc="lower center",bbox_to_anchor=(.48,1.00),frameon=False,ncol=3,fontsize=8)
    plt.rcParams["svg.hashsalt"]="p3-audit"
    svg = PAPER / "intervals.svg"
    fig.savefig(svg, metadata={"Date": None})
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines())+"\n")
    plt.close(fig)
    table("table_primary.typ",["Scenario","Test","Paired¹","Fallbacks","Uniform","Observed"],rows)
    table("table_design.typ",["Scenario","Checks","Initial","Minimax","Random","Observed interval"],width_rows)
    table("table_sensitivity.typ",["Scenario","5% slice","10% slice","All, 1%","Ref. solved","Sched. solved"],cap_rows)


if __name__=="__main__":
    main()
