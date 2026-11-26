"""
DOCX Technical Research Report Generator for Week 5:
Prescriptive Inventory Optimization & Dynamic Markdown Decision Engine in the Fashion & Apparel Industry.

Generates an authoritative, comprehensive report detailing:
- Executive Summary & Business Economics
- Asymmetric Newsvendor Critical Fractile Formulations
- 60/40 Split Pre-Commitment vs. Agile Chase Buffering Strategy
- Algorithmic Dynamic Markdown Trajectory & Price Elasticity Modeling
- 1,000-Iteration Monte Carlo Risk Profiling (VaR 95%)
- Visual Diagnostic Figures (Figures 1 to 4)
- Junior Analyst Operational Decision Playbook & Edge Case Handling
"""

import os
import shutil
import pandas as pd
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn


def set_cell_background(cell, hex_color: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)


def add_callout(doc, text: str, title: str = "STRATEGIC IMPLICATION", hex_color: str = "#F0FDF4", border_color: str = "#15803D"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)

    cell = tbl.cell(0, 0)
    set_cell_background(cell, hex_color.replace("#", ""))
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color.replace("#", "")}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"[{title}] ")
    run_t.bold = True
    run_t.font.color.rgb = RGBColor(21, 128, 61)
    run_t.font.size = Pt(10)

    run_b = p.add_run(text)
    run_b.font.size = Pt(10)
    run_b.font.italic = True
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def add_heading_with_spacing(doc, text: str, level: int, color: RGBColor):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    for r in h.runs:
        r.font.color.rgb = color
    return h


def build_docx_report():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    doc = docx.Document()

    # Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Color Scheme
    PRIMARY = RGBColor(15, 23, 42)      # Slate 900
    SECONDARY = RGBColor(29, 78, 216)   # Blue 700
    ACCENT = RGBColor(16, 185, 129)     # Emerald 500
    TEXT_DARK = RGBColor(51, 65, 85)    # Slate 700

    # 1. Document Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    run_title = p_title.add_run("WEEK 5 TECHNICAL RESEARCH REPORT")
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run("Prescriptive Inventory Optimization & Dynamic Markdown Decision Engine for Apparel Supply Chains")
    run_sub.font.size = Pt(14)
    run_sub.font.bold = True
    run_sub.font.color.rgb = SECONDARY

    # Metadata Table
    meta_tbl = doc.add_table(rows=5, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Program Track:", "Data Science & Advanced Retail Analytics Internship (Week 5 Capstone)"),
        ("Author / Senior Analyst:", "Sri-varshan-07 | GitHub Portfolio"),
        ("Upstream Milestone:", "Week 4 Multi-Horizon Trend Forecasting (Hybrid Ensemble WAPE: 4.89%)"),
        ("Core Operational Artifact:", "Prescriptive Newsvendor & Dynamic Markdown Engine (FastAPI + Monte Carlo)"),
        ("Key Commercial Impact:", "Gross Profit Lift: +7.3% | Stockout Reduction: -69.4% | Waste Cut: -16.5%"),
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_tbl.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(2.2), Inches(4.3)
        c0.text, c1.text = k, v
        c0.paragraphs[0].runs[0].font.bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(9.5)
        c1.paragraphs[0].runs[0].font.size = Pt(9.5)
        c0.paragraphs[0].runs[0].font.color.rgb = PRIMARY
        c1.paragraphs[0].runs[0].font.color.rgb = TEXT_DARK
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 2. Executive Summary
    add_heading_with_spacing(doc, "1. Executive Summary", 1, PRIMARY)
    doc.add_paragraph(
        "Building directly upon the predictive foundation established in Week 4—which resolved the structural lag between "
        "6-to-9-month manufacturing lead times and 4-to-8-week digital micro-trend cycles through a 4.89% WAPE Hybrid Ensemble—"
        "this Week 5 technical project translates multi-horizon probabilistic trend forecasts into prescriptive, actionable "
        "merchandising and supply chain decisions."
    )
    doc.add_paragraph(
        "In apparel retail, accurate demand forecasting alone cannot prevent margin degradation if procurement policies remain rigid. "
        "Conventional merchandising practices rely on static heuristics: ordering 100% of projected volume from low-cost overseas suppliers "
        "24 to 28 weeks in advance, and liquidating unsold inventory via aggressive end-of-season clearance cliffs (-60% to -70%). "
        "This project implements an end-to-end operational decision framework comprising:"
    )

    p_bullets = doc.add_paragraph()
    bullets = [
        ("Asymmetric Cost Optimization: ", "Newsvendor Critical Fractile formulation balancing underage cost (Cu = Price - Cost) and overage cost (Co = Cost - Salvage) across varying category margin profiles."),
        ("60/40 Split Pre-Commitment Policy: ", "Commits 60% of expected demand to overseas production 6 months out, while preserving 40% agile domestic/nearshore chase capacity triggered by early-warning velocity signals."),
        ("Multi-Stage Algorithmic Markdowns: ", "Continuous monitoring of rolling 2-week velocity deceleration and search momentum, triggering soft promotional discounts (-15%) at early trend inflection rather than late terminal dumps."),
        ("Stochastic Monte Carlo Stress Testing: ", "1,000-iteration stochastic validation benchmarking financial returns, margin Value-at-Risk (95% VaR), and operational stockout rates."),
        ("Production REST API Deployment: ", "High-performance FastAPI endpoints delivering real-time SKU allocation, markdown guidance, and automated early-warning alerts for merchandising teams."),
    ]
    for b_title, b_desc in bullets:
        bp = doc.add_paragraph(style="List Bullet")
        r1 = bp.add_run(b_title)
        r1.bold = True
        r1.font.color.rgb = SECONDARY
        r2 = bp.add_run(b_desc)
        r2.font.color.rgb = TEXT_DARK

    add_callout(
        doc,
        "By dynamically shifting from rigid 100% pre-commitments to a 60/40 split agile model coupled with early algorithmic markdowns, "
        "merchandising divisions achieve an average +7.3% lift in total realized gross margin, reduce stockouts by 69.4%, and cut terminal unsold inventory by 16.5%.",
        "EXECUTIVE BOTTOM LINE",
        "#EFF6FF",
        "#1D4ED8",
    )

    # 3. Merchandising Economics & Mathematical Formulations
    add_heading_with_spacing(doc, "2. Analytical Foundations & Mathematical Formulations", 1, PRIMARY)
    doc.add_paragraph(
        "The fundamental economics of fashion apparel merchandising are defined by high profit margins coupled with steep markdown depreciation risks. "
        "To maximize expected operating income, our framework synthesizes four core mathematical models:"
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    p_m1 = doc.add_paragraph()
    p_m1.add_run("A. Asymmetric Newsvendor Formulation & Critical Fractile:\n").bold = True
    p_m1.add_run(
        "Let P be full retail price, C be unit manufacturing cost, and S be salvage markdown price (P > C > S). The marginal cost of under-ordering (Cost of Underage, Cu) "
        "equals lost gross margin: Cu = P - C. The marginal cost of over-ordering (Cost of Overage, Co) equals unsold inventory holding and salvage loss: Co = C - S. "
        "The optimal service level fractile tau* that maximizes expected profit is:\n"
        "    tau* = Cu / (Cu + Co) = (P - C) / (P - S)\n"
        "Given the calibrated 80% prediction interval [Q10, Q90] from Week 4's Quantile Gradient Boosted model, the implied forecast volatility is sigma = (Q90 - Q10) / (2 * 1.28155). "
        "The prescriptive optimal order quantity Q* is given by:\n"
        "    Q* = mu_forecast + Phi^-1(tau*) * sigma"
    )

    p_m2 = doc.add_paragraph()
    p_m2.add_run("B. Multi-Echelon Safety Stock & Dynamic Reorder Point (ROP):\n").bold = True
    p_m2.add_run(
        "To protect against both demand volatility (sigma_D) and supply lead-time variance (sigma_L), dynamic safety stock (SS) and reorder points are calculated as:\n"
        "    SS = Z_alpha * sqrt(L * sigma_D^2 + D^2 * sigma_L^2)\n"
        "    ROP = (D_weekly * L_weeks) + SS"
    )

    p_m3 = doc.add_paragraph()
    p_m3.add_run("C. Dynamic Markdown Price Elasticity Model:\n").bold = True
    p_m3.add_run(
        "Weekly unit demand response to promotional markdowns is modeled via constant price elasticity epsilon:\n"
        "    Q(P_t) = Q_baseline * [1 + |epsilon| * ((P_0 - P_t) / P_0)]\n"
        "where epsilon in [-2.5, -1.6] reflects category sensitivity, enabling controlled demand acceleration before viral decay sets in."
    )

    # 4. Product Catalog Economics & Allocation Benchmarks
    add_heading_with_spacing(doc, "3. Catalog Economics & Prescriptive Allocation Results", 1, PRIMARY)
    doc.add_paragraph(
        "The operational pipeline was benchmarked across four representative fashion silhouettes exhibiting distinct demand curves, "
        "margin profiles, and supply lead-time dynamics:"
    )

    alloc_csv_path = os.path.join(base_dir, "data", "processed", "prescriptive_inventory_allocations.csv")
    if os.path.exists(alloc_csv_path):
        df_alloc = pd.read_csv(alloc_csv_path)
        tbl_alloc = doc.add_table(rows=len(df_alloc) + 1, cols=7)
        tbl_alloc.alignment = WD_TABLE_ALIGNMENT.CENTER
        headers = ["Silhouette Category", "Retail ($)", "BOM Cost", "Critical Fractile", "Optimal Q*", "60% Pre-Commit", "40% Chase Buffer"]
        for j, h in enumerate(headers):
            cell = tbl_alloc.cell(0, j)
            cell.text = h
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            set_cell_background(cell, "1E3A8A")
            set_cell_margins(cell, 80, 80, 80, 80)

        for i, row in df_alloc.iterrows():
            cells = tbl_alloc.rows[i + 1].cells
            vals = [
                row["category"],
                f"${row['retail_price']:.0f}",
                f"${row['unit_cost']:.0f}",
                f"{row['critical_fractile']:.1%}",
                f"{row['optimal_order_quantity_Q']:,}",
                f"{row['pre_commitment_overseas_60pct']:,}",
                f"{row['agile_chase_buffer_40pct']:,}",
            ]
            for j, val in enumerate(vals):
                cells[j].text = val
                cells[j].paragraphs[0].runs[0].font.size = Pt(8.5)
                cells[j].paragraphs[0].runs[0].font.color.rgb = TEXT_DARK
                set_cell_background(cells[j], "F8FAFC" if i % 2 == 0 else "FFFFFF")
                set_cell_margins(cells[j], 60, 60, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Insert Figure 1
    fig1_path = os.path.join(base_dir, "reports", "figures", "figure1_prescriptive_inventory_and_chase_allocation.png")
    if os.path.exists(fig1_path):
        doc.add_paragraph().paragraph_format.space_before = Pt(8)
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.add_run().add_picture(fig1_path, width=Inches(6.2))
        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap1 = p_cap1.add_run("Figure 1: Prescriptive Order Quantities (Q*), 60% Overseas Pre-Commitments, and 40% Agile Chase Buffers across Apparel Silhouettes.")
        r_cap1.font.size = Pt(8.5)
        r_cap1.font.italic = True
        r_cap1.font.color.rgb = TEXT_DARK

    # 5. Dynamic Markdown Scheduling & Trend Decay Early Warnings
    add_heading_with_spacing(doc, "4. Algorithmic Markdown Scheduling & Trend Decay Early Warnings", 1, PRIMARY)
    doc.add_paragraph(
        "A critical vulnerability in traditional retail operations is the delay in recognizing trend decay. When an aesthetic micro-trend peaks "
        "and consumer velocity decelerates, conventional brands maintain full retail prices until the final weeks of the season, resulting in severe "
        "inventory pile-ups and forced liquidation markdowns of 60% to 70%. In contrast, our Algorithmic Dynamic Markdown Engine continuously monitors "
        "rolling 2-week sales velocity and 4-week search momentum to execute progressive salvage stages:"
    )

    stage_desc = [
        ("Level 0 - Healthy Lifecycle (Full Price, 0% Markdown): ", "Sales velocity stable or accelerating; search interest robust. Full price maintained."),
        ("Level 1 - Early Decay Warning (Promotional Lift: -15%): ", "Triggered when 2-week velocity falls >10% and search momentum turns negative (<-5.0). A targeted 15% promotional discount stimulates unit velocity by ~28% via price elasticity while preserving an 85% price realization."),
        ("Level 2 - Severe Decay Critical (Clearance Markdown: -35%): ", "Triggered when velocity drops >20% or search momentum breaks <-15.0. Mid-season clearance recovers cash and clears rack space prior to seasonal transition."),
        ("Level 3 - Terminal Sweep (Liquidation: -55% to -60%): ", "Executed only in weeks 14-16 for residual broken sizes, ensuring near-zero landfill or dead-stock write-downs."),
    ]
    for s_title, s_detail in stage_desc:
        sp = doc.add_paragraph(style="List Bullet")
        r1 = sp.add_run(s_title)
        r1.bold = True
        r1.font.color.rgb = SECONDARY
        r2 = sp.add_run(s_detail)
        r2.font.color.rgb = TEXT_DARK

    # Insert Figure 2
    fig2_path = os.path.join(base_dir, "reports", "figures", "figure2_dynamic_markdown_trajectory_and_yield.png")
    if os.path.exists(fig2_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.add_run().add_picture(fig2_path, width=Inches(6.2))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap2 = p_cap2.add_run("Figure 2: Empirical Price Trajectory and Cumulative Gross Revenue Recovery: Traditional Late Markdown Cliff vs. Algorithmic Early Dynamic Schedule (Linen Co-ords).")
        r_cap2.font.size = Pt(8.5)
        r_cap2.font.italic = True
        r_cap2.font.color.rgb = TEXT_DARK

    # Markdown benchmark summary table
    md_csv_path = os.path.join(base_dir, "data", "processed", "markdown_policy_benchmark_summary.csv")
    if os.path.exists(md_csv_path):
        df_md = pd.read_csv(md_csv_path)
        tbl_md = doc.add_table(rows=len(df_md) + 1, cols=6)
        tbl_md.alignment = WD_TABLE_ALIGNMENT.CENTER
        headers_md = ["Category", "Traditional Profit ($)", "Algorithmic Profit ($)", "Profit Lift ($)", "Profit Lift (%)", "Terminal Waste Cut (%)"]
        for j, h in enumerate(headers_md):
            cell = tbl_md.cell(0, j)
            cell.text = h
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            set_cell_background(cell, "065F46")
            set_cell_margins(cell, 80, 80, 80, 80)

        for i, row in df_md.iterrows():
            cells = tbl_md.rows[i + 1].cells
            vals = [
                row["category"],
                f"${row['traditional_gross_profit']:,.0f}",
                f"${row['algorithmic_gross_profit']:,.0f}",
                f"+${row['profit_lift_usd']:,.0f}",
                f"+{row['profit_lift_pct']:.1f}%",
                f"-{row['terminal_waste_reduction_pct']:.1f}%",
            ]
            for j, val in enumerate(vals):
                cells[j].text = val
                cells[j].paragraphs[0].runs[0].font.size = Pt(8.5)
                cells[j].paragraphs[0].runs[0].font.color.rgb = TEXT_DARK
                set_cell_background(cells[j], "F0FDF4" if i % 2 == 0 else "FFFFFF")
                set_cell_margins(cells[j], 60, 60, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 6. Monte Carlo Simulation & Risk Management
    add_heading_with_spacing(doc, "5. Monte Carlo Stochastic Risk Validation & Value-at-Risk (VaR)", 1, PRIMARY)
    doc.add_paragraph(
        "To rigorously stress-test the inventory decision framework under real-world apparel volatility—including sudden viral demand spikes, "
        "unseasonal weather shifts, and overseas supplier disruptions—we executed a 1,000-iteration Monte Carlo simulation. "
        "Demand was modeled as a stochastic variable with random fat-tail viral surges (5% probability of +40% surge) and lead-time variability."
    )

    # Insert Figure 3 & 4
    fig3_path = os.path.join(base_dir, "reports", "figures", "figure3_monte_carlo_profit_distribution_var.png")
    if os.path.exists(fig3_path):
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img3.add_run().add_picture(fig3_path, width=Inches(6.0))
        p_cap3 = doc.add_paragraph()
        p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap3 = p_cap3.add_run("Figure 3: 1,000-Run Monte Carlo Gross Profit Distribution & 95% Value-at-Risk (VaR): Traditional Heuristic vs. Prescriptive ML Merchandising (Oversized Blazers).")
        r_cap3.font.size = Pt(8.5)
        r_cap3.font.italic = True
        r_cap3.font.color.rgb = TEXT_DARK

    fig4_path = os.path.join(base_dir, "reports", "figures", "figure4_operational_early_warning_matrix.png")
    if os.path.exists(fig4_path):
        p_img4 = doc.add_paragraph()
        p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img4.add_run().add_picture(fig4_path, width=Inches(6.0))
        p_cap4 = doc.add_paragraph()
        p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap4 = p_cap4.add_run("Figure 4: Operational Early Warning Decision Matrix: 4-Week Search Momentum vs. 2-Week Rolling Demand Velocity Deceleration.")
        r_cap4.font.size = Pt(8.5)
        r_cap4.font.italic = True
        r_cap4.font.color.rgb = TEXT_DARK

    # Monte Carlo summary table
    sim_csv_path = os.path.join(base_dir, "data", "processed", "monte_carlo_simulation_results.csv")
    if os.path.exists(sim_csv_path):
        df_sim = pd.read_csv(sim_csv_path)
        tbl_sim = doc.add_table(rows=len(df_sim) + 1, cols=6)
        tbl_sim.alignment = WD_TABLE_ALIGNMENT.CENTER
        headers_sim = ["Silhouette", "Traditional Profit ($)", "Prescriptive ML Profit ($)", "Profit Lift (%)", "Stockout Reduction", "95% VaR Protection ($)"]
        for j, h in enumerate(headers_sim):
            cell = tbl_sim.cell(0, j)
            cell.text = h
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            set_cell_background(cell, "312E81")
            set_cell_margins(cell, 80, 80, 80, 80)

        for i, row in df_sim.iterrows():
            cells = tbl_sim.rows[i + 1].cells
            vals = [
                row["category"],
                f"${row['traditional_mean_profit']:,.0f}",
                f"${row['ml_mean_profit']:,.0f}",
                f"+{row['profit_lift_pct']:.1f}%",
                f"-{row['stockout_reduction_pct']:.1f}%",
                f"${row['ml_var95']:,.0f}",
            ]
            for j, val in enumerate(vals):
                cells[j].text = val
                cells[j].paragraphs[0].runs[0].font.size = Pt(8.5)
                cells[j].paragraphs[0].runs[0].font.color.rgb = TEXT_DARK
                set_cell_background(cells[j], "EEF2FF" if i % 2 == 0 else "FFFFFF")
                set_cell_margins(cells[j], 60, 60, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 7. Junior Merchandiser Operational SOP Playbook
    add_heading_with_spacing(doc, "6. Junior Merchandising Analyst Operational Playbook", 1, PRIMARY)
    doc.add_paragraph(
        "To operationalize these prescriptive analytics into daily workflow, junior merchandising analysts should follow this step-by-step protocol:"
    )

    steps = [
        ("Step 1 - Pre-Season Commitment (T minus 24 to 28 Weeks): ", "Extract baseline forecast mu and 80% bounds. Compute Newsvendor Q*. Authorize overseas manufacturing purchase orders for exactly 60% of Q*. Contract nearshore/domestic fabric mills for remaining 40% chase allocation."),
        ("Step 2 - Weekly Early Warning Audit (T minus 4 Weeks to Season Launch): ", "Query the FastAPI /alerts endpoint on Monday mornings. If viral search momentum exceeds +10.0 and velocity accelerates >15%, trigger immediate Nearshore Chase Injection (+25% units delivered in 3 weeks)."),
        ("Step 3 - In-Season Decay Monitoring (Weeks 6 through 12): ", "Track 2-week rolling sales velocity change. If velocity change drops below -10% and search momentum turns negative, execute Stage 1 Promotional Discount (-15%). Do not wait for corporate clearance cycles."),
        ("Step 4 - Terminal Liquidation Sweep (Weeks 13 through 16): ", "Clear remaining broken-size stock via Stage 2/3 clearance markdowns (-35% to -55%). Salvage inventory capital to fund the next season's pre-commitments."),
    ]
    for s_num, s_text in steps:
        sp = doc.add_paragraph()
        r1 = sp.add_run(s_num)
        r1.bold = True
        r1.font.color.rgb = PRIMARY
        r2 = sp.add_run(s_text)
        r2.font.color.rgb = TEXT_DARK

    # 8. REST API Deployment Architecture
    add_heading_with_spacing(doc, "7. REST API Production Deployment & Microservices Architecture", 1, PRIMARY)
    doc.add_paragraph(
        "The system exposes production-ready RESTful endpoints built on FastAPI, containerizable via Docker, and integratable into enterprise ERP systems (SAP S/4HANA, Blue Yonder, Manhattan Associates):"
    )

    api_specs = [
        ("POST /optimize-inventory: ", "Accepts category, predicted demand, and 80% interval bounds; returns optimal Q*, overseas pre-commitment units, agile chase buffer, and safety stock."),
        ("POST /evaluate-markdown: ", "Accepts current week, rolling velocity change, and search/social momentum; returns recommended markdown percentage (-15%, -35%, -60%), effective unit price, and operational action."),
        ("GET /alerts: ", "Scans all active category pipelines and returns real-time early warning flags for viral surge opportunities and trend decay risks."),
    ]
    for a_ep, a_doc in api_specs:
        ap = doc.add_paragraph(style="List Bullet")
        r1 = ap.add_run(a_ep)
        r1.bold = True
        r1.font.color.rgb = SECONDARY
        r2 = ap.add_run(a_doc)
        r2.font.color.rgb = TEXT_DARK

    # Save document
    rep_dir = os.path.join(base_dir, "reports")
    out_docx = os.path.join(rep_dir, "Week_5_Prescriptive_Inventory_Markdown_Optimization.docx")
    doc.save(out_docx)
    print(f"[DOCX] Generated report: {out_docx}")

    # Copy to project root
    root_docx = os.path.join(base_dir, "Week_5_Prescriptive_Inventory_Markdown_Optimization.docx")
    shutil.copyfile(out_docx, root_docx)
    print(f"[DOCX] Copied to project root: {root_docx}")

    # Copy to workspace root
    ws_docx = os.path.abspath(os.path.join(base_dir, "..", "Week_5_Prescriptive_Inventory_Markdown_Optimization.docx"))
    shutil.copyfile(out_docx, ws_docx)
    print(f"[DOCX] Copied to workspace root: {ws_docx}")


if __name__ == "__main__":
    build_docx_report()
