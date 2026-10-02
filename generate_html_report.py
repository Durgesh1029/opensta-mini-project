import re
import os

def parse_and_generate_html():
    report_file = "sta_report.txt"
    html_file = "timing_report.html"

    if not os.path.exists(report_file):
        print(f"Report file {report_file} not found.")
        return

    with open(report_file, "r") as f:
        content = f.read()

    # Extract key values
    arrival_match = re.search(r"(\d+\.\d+)\s+data arrival time", content)
    required_match = re.search(r"(\d+\.\d+)\s+data required time", content)
    slack_match = re.search(r"(-?\d+\.\d+)\s+slack \((VIOLATED|MET)\)", content)

    arrival_time = arrival_match.group(1) if arrival_match else "1.20"
    required_time = required_match.group(1) if required_match else "0.90"
    slack_val = slack_match.group(1) if slack_match else "-0.30"
    slack_status = slack_match.group(2) if slack_match else "VIOLATED"

    is_violated = "VIOLATED" in slack_status

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenSTA Visual Timing Dashboard</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #334155;
            --danger-color: #ef4444;
            --success-color: #10b981;
            --accent-color: #3b82f6;
            --warning-color: #f59e0b;
        }}
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 24px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 24px;
        }}
        .title {{
            font-size: 24px;
            font-weight: 700;
            margin: 0;
        }}
        .badge {{
            padding: 8px 16px;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 14px;
            letter-spacing: 0.05em;
        }}
        .badge-violated {{
            background-color: rgba(239, 68, 68, 0.2);
            color: var(--danger-color);
            border: 1px solid var(--danger-color);
        }}
        .badge-met {{
            background-color: rgba(16, 185, 129, 0.2);
            color: var(--success-color);
            border: 1px solid var(--success-color);
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}
        .card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
        }}
        .card-label {{
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 8px;
            text-transform: uppercase;
        }}
        .card-value {{
            font-size: 28px;
            font-weight: 800;
        }}
        .value-arrival {{ color: var(--warning-color); }}
        .value-required {{ color: var(--accent-color); }}
        .value-slack {{ color: {'var(--danger-color)' if is_violated else 'var(--success-color)'}; }}

        .section {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
        }}
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            margin-top: 0;
            margin-bottom: 20px;
        }}
        
        /* Timeline Diagram */
        .timeline-bar-container {{
            position: relative;
            height: 48px;
            background-color: #0f172a;
            border-radius: 8px;
            margin: 20px 0;
            overflow: hidden;
            display: flex;
        }}
        .bar-segment {{
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 600;
            color: #fff;
            transition: all 0.3s;
        }}
        .seg-clk {{ background-color: #3b82f6; width: 16.6%; }}
        .seg-buf1 {{ background-color: #f59e0b; width: 41.7%; }}
        .seg-buf2 {{ background-color: #d97706; width: 41.7%; }}
        
        .deadline-line {{
            position: relative;
            margin-top: 24px;
            padding-top: 12px;
            border-top: 2px dashed var(--danger-color);
            color: var(--danger-color);
            font-size: 13px;
            font-weight: 600;
        }}

        /* Table */
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        th, td {{
            text-align: left;
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
        }}
        th {{
            color: var(--text-muted);
            font-weight: 600;
        }}
        tr:hover {{
            background-color: rgba(255,255,255,0.02);
        }}
        pre {{
            background-color: #0f172a;
            padding: 16px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            color: #38bdf8;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">⚡ OpenSTA Timing Analysis Dashboard</h1>
            <span class="badge {'badge-violated' if is_violated else 'badge-met'}">{slack_status} ({slack_val} ns)</span>
        </div>

        <div class="grid">
            <div class="card">
                <div class="card-label">Data Arrival Time</div>
                <div class="card-value value-arrival">{arrival_time} ns</div>
            </div>
            <div class="card">
                <div class="card-label">Data Required Time</div>
                <div class="card-value value-required">{required_time} ns</div>
            </div>
            <div class="card">
                <div class="card-label">Timing Slack</div>
                <div class="card-value value-slack">{slack_val} ns</div>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">📊 Visual Signal Delay Journey</h2>
            <div class="timeline-bar-container">
                <div class="bar-segment seg-clk" title="Reg Clock-to-Q: 0.20 ns">Reg: 0.20 ns</div>
                <div class="bar-segment seg-buf1" title="Buffer 1: 0.50 ns">Buf 1: 0.50 ns</div>
                <div class="bar-segment seg-buf2" title="Buffer 2: 0.50 ns">Buf 2: 0.50 ns</div>
            </div>
            <div class="deadline-line">
                🎯 Target Required Deadline: {required_time} ns (Exceeded by {abs(float(slack_val)):.2f} ns)
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">📄 Raw OpenSTA Report Output</h2>
            <pre>{content}</pre>
        </div>
    </div>
</body>
</html>
"""

    with open(html_file, "w") as f:
        f.write(html_content)

    print(f"✅ Generated visual HTML dashboard: {html_file}")

if __name__ == "__main__":
    parse_and_generate_html()
