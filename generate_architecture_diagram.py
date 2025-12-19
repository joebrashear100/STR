#!/usr/bin/env python3
"""
Generate O365 Daily Digest Architecture Diagram
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import matplotlib.lines as mlines

# Create figure with high resolution
fig, ax = plt.subplots(1, 1, figsize=(20, 28))
ax.set_xlim(0, 100)
ax.set_ylim(0, 140)
ax.axis('off')

# Color scheme - professional blue theme
COLORS = {
    'header': '#1a365d',
    'header_text': '#ffffff',
    'trigger': '#3182ce',
    'flow_bg': '#ebf8ff',
    'flow_border': '#2b6cb0',
    'init': '#4299e1',
    'outlook': '#0078d4',
    'teams': '#6264a7',
    'ai': '#10b981',
    'output': '#ed8936',
    'error': '#e53e3e',
    'data': '#805ad5',
    'connection': '#38a169',
    'env': '#d69e2e',
    'text': '#2d3748',
    'light_text': '#4a5568',
    'white': '#ffffff',
    'light_bg': '#f7fafc',
}

def draw_rounded_box(ax, x, y, width, height, color, text='', fontsize=10,
                      text_color='white', alpha=1.0, linewidth=2, edgecolor=None):
    """Draw a rounded rectangle with centered text"""
    if edgecolor is None:
        edgecolor = color
    box = FancyBboxPatch((x, y), width, height,
                          boxstyle="round,pad=0.02,rounding_size=0.5",
                          facecolor=color, edgecolor=edgecolor,
                          linewidth=linewidth, alpha=alpha)
    ax.add_patch(box)
    if text:
        lines = text.split('\n')
        line_height = fontsize * 0.04
        total_height = len(lines) * line_height
        start_y = y + height/2 + total_height/2 - line_height/2
        for i, line in enumerate(lines):
            ax.text(x + width/2, start_y - i*line_height, line,
                   ha='center', va='center', fontsize=fontsize,
                   color=text_color, fontweight='bold', wrap=True)

def draw_arrow(ax, start, end, color='#4a5568'):
    """Draw an arrow between two points"""
    ax.annotate('', xy=end, xytext=start,
               arrowprops=dict(arrowstyle='->', color=color, lw=2))

# ============= HEADER =============
draw_rounded_box(ax, 5, 133, 90, 5, COLORS['header'],
                 'O365 DAILY DIGEST ARCHITECTURE\nVersion 1.2.0.7', 14, COLORS['header_text'])

# ============= SCHEDULED TRIGGER =============
draw_rounded_box(ax, 40, 125, 20, 5, COLORS['trigger'],
                 'SCHEDULED TRIGGER\n(Daily 5PM)', 10)

draw_arrow(ax, (50, 125), (50, 122))

# ============= MAIN FLOW BOX =============
main_flow = FancyBboxPatch((5, 42), 90, 78,
                            boxstyle="round,pad=0.01,rounding_size=1",
                            facecolor=COLORS['flow_bg'], edgecolor=COLORS['flow_border'],
                            linewidth=3, alpha=0.7)
ax.add_patch(main_flow)

# Flow title
ax.text(50, 117, 'POWER AUTOMATE CLOUD FLOW', ha='center', va='center',
       fontsize=13, color=COLORS['flow_border'], fontweight='bold')
ax.text(50, 114.5, '(GetEmailsOneNoteSched)', ha='center', va='center',
       fontsize=10, color=COLORS['light_text'], fontweight='normal')

# ============= INITIALIZATION SECTION =============
init_box = FancyBboxPatch((8, 105, ), 84, 7,
                           boxstyle="round,pad=0.01,rounding_size=0.3",
                           facecolor=COLORS['white'], edgecolor=COLORS['init'],
                           linewidth=2, alpha=0.9)
ax.add_patch(init_box)
ax.text(50, 110.5, 'INITIALIZATION', ha='center', va='center',
       fontsize=11, color=COLORS['init'], fontweight='bold')

# Init boxes
draw_rounded_box(ax, 12, 106, 18, 3.5, COLORS['init'], 'Get User\nProfile', 8)
draw_rounded_box(ax, 33, 106, 18, 3.5, COLORS['init'], 'Init Email\nDigest Var', 8)
draw_rounded_box(ax, 54, 106, 18, 3.5, COLORS['init'], 'Init Teams\nDigest Var', 8)

# Arrows between init boxes
draw_arrow(ax, (30, 107.75), (33, 107.75), COLORS['init'])
draw_arrow(ax, (51, 107.75), (54, 107.75), COLORS['init'])

# Arrow down from init
draw_arrow(ax, (50, 105), (50, 102))

# ============= PARALLEL PROCESSING SECTION =============
# Fork arrows
draw_arrow(ax, (50, 102), (27, 98), COLORS['outlook'])
draw_arrow(ax, (50, 102), (73, 98), COLORS['teams'])

# ============= OUTLOOK SECTION (Left) =============
# Outlook connector box
draw_rounded_box(ax, 10, 93, 34, 4, COLORS['outlook'],
                 'OUTLOOK CONNECTOR (If Enabled)', 9)

draw_arrow(ax, (27, 93), (27, 90))

# Get Recent Emails
draw_rounded_box(ax, 10, 85, 34, 4.5, '#2c5282',
                 'Get Recent Emails\n(Last 24 Hours) - Inbox Top 1000', 8)

draw_arrow(ax, (27, 85), (27, 82))

# For Each Email
draw_rounded_box(ax, 10, 75, 34, 6.5, '#2b6cb0',
                 'For Each Email:\n- Extract From\n- Extract Subject\n- Extract Body\n- Append to Digest', 7)

draw_arrow(ax, (27, 75), (27, 72))

# AI Builder Emails
ai_email_box = FancyBboxPatch((10, 65), 34, 6,
                               boxstyle="round,pad=0.01,rounding_size=0.3",
                               facecolor=COLORS['white'], edgecolor=COLORS['ai'],
                               linewidth=2)
ax.add_patch(ai_email_box)
ax.text(27, 69.5, 'AI BUILDER', ha='center', va='center',
       fontsize=9, color=COLORS['ai'], fontweight='bold')
draw_rounded_box(ax, 13, 66, 28, 3, COLORS['ai'],
                 'SummarizeEmails\n(GPT-4.1 Mini)', 7)

# ============= TEAMS SECTION (Right) =============
# Teams connector box
draw_rounded_box(ax, 56, 93, 34, 4, COLORS['teams'],
                 'TEAMS CONNECTOR (If Enabled)', 9)

draw_arrow(ax, (73, 93), (73, 90))

# Get Recent Chats
draw_rounded_box(ax, 56, 85, 34, 4.5, '#553c9a',
                 'Get Recent Chats\n(Graph API) - Last 24 Hours', 8)

draw_arrow(ax, (73, 85), (73, 82))

# For Each Chat
draw_rounded_box(ax, 56, 75, 34, 6.5, '#6b46c1',
                 'For Each Chat:\n- Get Messages\n- Parse Content\n- Filter by Date\n- Append to Digest', 7)

draw_arrow(ax, (73, 75), (73, 72))

# AI Builder Teams
ai_teams_box = FancyBboxPatch((56, 65), 34, 6,
                               boxstyle="round,pad=0.01,rounding_size=0.3",
                               facecolor=COLORS['white'], edgecolor=COLORS['ai'],
                               linewidth=2)
ax.add_patch(ai_teams_box)
ax.text(73, 69.5, 'AI BUILDER', ha='center', va='center',
       fontsize=9, color=COLORS['ai'], fontweight='bold')
draw_rounded_box(ax, 59, 66, 28, 3, COLORS['ai'],
                 'SummarizeTeams\n(Reasoning Model)', 7)

# ============= MERGE AND FINAL PROCESSING =============
# Merge arrows
draw_arrow(ax, (27, 65), (40, 61), COLORS['ai'])
draw_arrow(ax, (73, 65), (60, 61), COLORS['ai'])

# Final AI Builder
ai_final_box = FancyBboxPatch((30, 54), 40, 6,
                               boxstyle="round,pad=0.01,rounding_size=0.3",
                               facecolor=COLORS['white'], edgecolor=COLORS['ai'],
                               linewidth=2)
ax.add_patch(ai_final_box)
ax.text(50, 58.5, 'AI BUILDER', ha='center', va='center',
       fontsize=9, color=COLORS['ai'], fontweight='bold')
draw_rounded_box(ax, 33, 55, 34, 3, COLORS['ai'],
                 'SummarizeO365Content (GPT-4.1 Mini)', 7)

draw_arrow(ax, (50, 54), (50, 52))

# Apply HTML Styling
draw_rounded_box(ax, 33, 48, 34, 3.5, COLORS['output'],
                 'Apply HTML Styling\n(Format for Email)', 8)

draw_arrow(ax, (50, 48), (50, 45.5))

# Send Daily Digest
draw_rounded_box(ax, 33, 43, 34, 3, COLORS['output'],
                 'Send Daily Digest (Outlook Email)', 8)

# ============= ERROR HANDLING =============
error_box = FancyBboxPatch((8, 42.5), 84, 3,
                            boxstyle="round,pad=0.01,rounding_size=0.3",
                            facecolor='#fff5f5', edgecolor=COLORS['error'],
                            linewidth=2)
ax.add_patch(error_box)
ax.text(50, 44, 'ERROR HANDLING: On Failure - Send error notification email with run details',
       ha='center', va='center', fontsize=8, color=COLORS['error'], fontweight='bold')

# ============= DATA SOURCES SECTION =============
data_box = FancyBboxPatch((5, 30), 90, 10,
                           boxstyle="round,pad=0.01,rounding_size=0.5",
                           facecolor=COLORS['light_bg'], edgecolor=COLORS['data'],
                           linewidth=2)
ax.add_patch(data_box)
ax.text(50, 38.5, 'DATA SOURCES', ha='center', va='center',
       fontsize=11, color=COLORS['data'], fontweight='bold')

draw_rounded_box(ax, 10, 31, 24, 5, COLORS['data'],
                 'OUTLOOK MAILBOX\nUser\'s own inbox only', 8)
draw_rounded_box(ax, 38, 31, 24, 5, '#7c3aed',
                 'TEAMS CHATS\nUser\'s own chats only', 8)
draw_rounded_box(ax, 66, 31, 24, 5, '#9f7aea',
                 'DATAVERSE (AI Models)\nCustom AI Prompts', 8)

# ============= CONNECTION REFERENCES =============
conn_box = FancyBboxPatch((5, 19), 90, 9,
                           boxstyle="round,pad=0.01,rounding_size=0.5",
                           facecolor=COLORS['light_bg'], edgecolor=COLORS['connection'],
                           linewidth=2)
ax.add_patch(conn_box)
ax.text(50, 26.5, 'CONNECTION REFERENCES', ha='center', va='center',
       fontsize=11, color=COLORS['connection'], fontweight='bold')

connections = [
    ('cr2de_O365Connector', 'Office 365 Users API'),
    ('cr2de_OutlookConnector', 'Office 365 Outlook API'),
    ('cr2de_TeamsConnector', 'Microsoft Teams (Graph API)'),
    ('mccia_Office365SEDB', 'Common Data Service (AI Builder)')
]

y_pos = 24
for ref, api in connections:
    ax.text(15, y_pos, f'{ref}', ha='left', va='center',
           fontsize=7, color=COLORS['text'], fontweight='bold', family='monospace')
    ax.text(45, y_pos, '→', ha='center', va='center',
           fontsize=10, color=COLORS['connection'], fontweight='bold')
    ax.text(50, y_pos, api, ha='left', va='center',
           fontsize=7, color=COLORS['light_text'])
    y_pos -= 1.5

# ============= ENVIRONMENT VARIABLES =============
env_box = FancyBboxPatch((5, 11), 90, 6,
                          boxstyle="round,pad=0.01,rounding_size=0.5",
                          facecolor=COLORS['light_bg'], edgecolor=COLORS['env'],
                          linewidth=2)
ax.add_patch(env_box)
ax.text(50, 15.5, 'ENVIRONMENT VARIABLES', ha='center', va='center',
       fontsize=11, color=COLORS['env'], fontweight='bold')

env_vars = [
    ('cr2de_IncludeOutlook', 'Enable/Disable Outlook mining (Boolean)'),
    ('cr2de_IncludeTeams', 'Enable/Disable Teams mining (Boolean)'),
    ('cr2de_ScheduleTimeUTC', 'Daily trigger time (Default: 21:00 UTC)')
]

x_positions = [12, 38, 64]
for i, (var, desc) in enumerate(env_vars):
    ax.text(x_positions[i], 13.5, var, ha='left', va='center',
           fontsize=6, color=COLORS['text'], fontweight='bold', family='monospace')
    ax.text(x_positions[i], 12.2, desc, ha='left', va='center',
           fontsize=5.5, color=COLORS['light_text'])

# ============= OUTPUT SECTION =============
output_box = FancyBboxPatch((5, 1), 90, 8.5,
                             boxstyle="round,pad=0.01,rounding_size=0.5",
                             facecolor=COLORS['light_bg'], edgecolor=COLORS['output'],
                             linewidth=2)
ax.add_patch(output_box)
ax.text(50, 8, 'OUTPUT: DAILY DIGEST EMAIL', ha='center', va='center',
       fontsize=11, color=COLORS['output'], fontweight='bold')

# Output details - left column
ax.text(10, 6.2, 'Subject: Daily Digest', ha='left', fontsize=7, color=COLORS['text'])
ax.text(10, 5.2, 'Importance: High', ha='left', fontsize=7, color=COLORS['text'])
ax.text(10, 4.2, 'Format: HTML', ha='left', fontsize=7, color=COLORS['text'])

# Output sections - right side
ax.text(40, 6.5, 'Sections:', ha='left', fontsize=7, color=COLORS['text'], fontweight='bold')
sections = [
    'Overview of the Day',
    'Major Actions and Decisions',
    'System or Technical Notes',
    'Collaboration and Communications',
    'Awareness and Announcements',
    'Stand-Up for Tomorrow Morning'
]
for i, section in enumerate(sections):
    col = 0 if i < 3 else 1
    row = i % 3
    x = 43 + col * 25
    y = 5.5 - row * 1.2
    ax.text(x, y, f'• {section}', ha='left', fontsize=6, color=COLORS['light_text'])

plt.tight_layout()
plt.savefig('/home/user/STR/O365_Daily_Digest_Architecture.png',
            dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("Diagram saved to: /home/user/STR/O365_Daily_Digest_Architecture.png")
