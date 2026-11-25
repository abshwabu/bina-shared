import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path="Bina_ERP_Modules_and_Integration_Guide.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Brand Colors
    C_BG_DARK = RGBColor(11, 19, 43)       # #0B132B Dark Navy Hero
    C_BG_LIGHT = RGBColor(248, 250, 252)   # #F8FAFC Off-white
    C_CARD_BG = RGBColor(255, 255, 255)    # Pure White
    C_CARD_BORDER = RGBColor(226, 232, 240)# Light Gray Border
    
    C_PRIMARY = RGBColor(2, 132, 199)      # #0284C7 Vibrant Blue/Cyan
    C_PRIMARY_DARK = RGBColor(3, 105, 161) # #0369A1 Darker Blue
    C_PRIMARY_LIGHT = RGBColor(224, 242, 254) # Light Blue Tint
    
    C_TEXT_DARK = RGBColor(15, 23, 42)     # #0F172A Slate 900
    C_TEXT_MUTED = RGBColor(100, 116, 139) # #64748B Slate 500
    C_TEXT_LIGHT = RGBColor(255, 255, 255)
    
    # Pillar Colors
    C_REV = RGBColor(16, 185, 129)         # Emerald Green (Revenue)
    C_REV_LIGHT = RGBColor(236, 253, 245)
    C_OPS = RGBColor(245, 158, 11)         # Amber (Operations)
    C_OPS_LIGHT = RGBColor(254, 243, 199)
    C_HR = RGBColor(139, 92, 246)          # Violet (People)
    C_HR_LIGHT = RGBColor(245, 243, 255)
    C_FIN = RGBColor(99, 102, 241)         # Indigo (Finance)
    C_FIN_LIGHT = RGBColor(238, 242, 255)
    C_ALERT = RGBColor(239, 68, 68)        # Red/Rose
    C_ALERT_LIGHT = RGBColor(254, 242, 242)

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category, slide_num=None):
        # Category Pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.2), Inches(0.35))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_PRIMARY_LIGHT
        pill.line.fill.background()
        tf = pill.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_PRIMARY_DARK
        p.alignment = PP_ALIGN.CENTER
        
        # Slide Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(10.5), Inches(0.6))
        tf_t = tb.text_frame
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEXT_DARK
        
        # Branding Tag on top right
        tag_tb = slide.shapes.add_textbox(Inches(9.5), Inches(0.4), Inches(3.0), Inches(0.4))
        tf_tag = tag_tb.text_frame
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = "BINA ERP | SALES & MARKETING DECK"
        p_tag.font.size = Pt(9)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_TEXT_MUTED
        p_tag.alignment = PP_ALIGN.RIGHT

        # Thin header separator line
        sep = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02))
        sep.fill.solid()
        sep.fill.fore_color.rgb = C_CARD_BORDER
        sep.line.fill.background()

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Executive Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_BG_DARK)

    # Decorative Cyan Accent Bar
    accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.5), Inches(0.8), Inches(0.08))
    accent.fill.solid()
    accent.fill.fore_color.rgb = C_PRIMARY
    accent.line.fill.background()

    # Title & Subtitle Box
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(2.8))
    tf = t_box.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "Bina ERP Platform"
    p0.font.size = Pt(38)
    p0.font.bold = True
    p0.font.color.rgb = C_TEXT_LIGHT

    p1 = tf.add_paragraph()
    p1.text = "Comprehensive Module Ecosystem & Sales Playbook"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(56, 189, 248) # Cyan

    p2 = tf.add_paragraph()
    p2.text = "How Every Module Works, Why Businesses Buy, and How Seamless Integrations Power Growth"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(203, 213, 225) # Slate 300

    # 3 Value Badges at bottom
    badges = [
        ("ZERO DATA SILOS", "One unified database. Enter data once, updates everywhere in real-time.", C_PRIMARY),
        ("RETAIL TO ENTERPRISE", "From 15-minute touch POS to full manufacturing BOMs & accounting.", C_REV),
        ("BUILT FOR PROFIT & TAX", "100% compliant with Ethiopian TIN, 15% VAT, and automated payroll.", C_FIN)
    ]
    for i, (b_title, b_desc, b_color) in enumerate(badges):
        bx = Inches(1.0 + i * 3.9)
        b_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, Inches(4.8), Inches(3.6), Inches(1.8))
        b_card.fill.solid()
        b_card.fill.fore_color.rgb = RGBColor(22, 33, 62)
        b_card.line.color.rgb = b_color
        b_card.line.width = Pt(1.5)
        
        btf = b_card.text_frame
        btf.word_wrap = True
        bp0 = btf.paragraphs[0]
        bp0.text = b_title
        bp0.font.size = Pt(12)
        bp0.font.bold = True
        bp0.font.color.rgb = b_color
        
        bp1 = btf.add_paragraph()
        bp1.text = b_desc
        bp1.font.size = Pt(10)
        bp1.font.color.rgb = RGBColor(226, 232, 240)

    add_notes(s1, 
        "PRESENTER OPENING SCRIPT:\n"
        "Welcome team! Today we are doing a deep dive into Bina ERP. As marketing and sales professionals, "
        "our job is not just to talk about software features; it's to show business owners how Bina ERP solves "
        "their biggest headaches—stock theft, manual data entry, lost sales, tax calculation nightmares, and "
        "disconnected departments. By the end of this presentation, you will clearly understand every single "
        "module, how they communicate with each other automatically, and the exact words to say to close deals."
    )

    # =========================================================================
    # SLIDE 2: THE PROBLEM WE SOLVE (The "Silo Tax")
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_BG_LIGHT)
    add_header(s2, "The Real Problem: The Costly 'Silo Tax' Businesses Face Today", "Market Context & Why Clients Buy")

    # Left Column: The Problem (Broken Silos)
    p_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2))
    p_box.fill.solid()
    p_box.fill.fore_color.rgb = C_ALERT_LIGHT
    p_box.line.color.rgb = C_ALERT
    p_box.line.width = Pt(1.5)
    
    ptf = p_box.text_frame
    ptf.word_wrap = True
    pp = ptf.paragraphs[0]
    pp.text = "BEFORE BINA ERP: FRAGMENTED CHAOS"
    pp.font.size = Pt(13)
    pp.font.bold = True
    pp.font.color.rgb = C_ALERT

    silo_points = [
        ("Stock Theft & Mystery Discrepancies", "Inventory in spreadsheets doesn't match what cashiers sell. Thousands lost every month."),
        ("Double & Triple Data Re-Entry", "Sales rep writes an invoice on paper, accountant retypes it into QuickBooks, warehouse retypes it again."),
        ("Blind Executive Decision Making", "Business owners don't know their real daily profit or top-selling products until 3 weeks after month-end."),
        ("Offline Nightmare & System Crashes", "When store Wi-Fi cuts out, cash registers freeze, lines back up, and sales are completely lost.")
    ]
    for title, desc in silo_points:
        p_t = ptf.add_paragraph()
        p_t.text = f"• {title}"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEXT_DARK
        p_d = ptf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_TEXT_MUTED

    # Right Column: The Bina ERP Solution
    s_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.2))
    s_box.fill.solid()
    s_box.fill.fore_color.rgb = C_REV_LIGHT
    s_box.line.color.rgb = C_REV
    s_box.line.width = Pt(1.5)
    
    stf = s_box.text_frame
    stf.word_wrap = True
    sp = stf.paragraphs[0]
    sp.text = "WITH BINA ERP: ONE UNIFIED ECOSYSTEM"
    sp.font.size = Pt(13)
    sp.font.bold = True
    sp.font.color.rgb = C_REV

    bina_points = [
        ("Instant Real-Time Stock Tracking", "Every item beeped at checkout instantly subtracts from central stock. Low-stock alerts trigger automatically."),
        ("Zero Manual Retyping (Lead-to-Cash)", "A lead in CRM converts to an invoice in 1 click, updates accounting journals, and logs cash in the bank."),
        ("Instant Profit & Loss on Owner's Phone", "Live P&L, balance sheets, and cashier reconciliations available at any second from anywhere."),
        ("100% Offline-Resilient POS Engine", "Cashiers keep scanning barcodes and printing receipts even when the internet drops. Syncs smoothly when back.")
    ]
    for title, desc in bina_points:
        p_t = stf.add_paragraph()
        p_t.text = f"✓ {title}"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEXT_DARK
        p_d = stf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_TEXT_MUTED

    add_notes(s2,
        "TALKING POINTS FOR SALES:\n"
        "Ask the prospect: 'How many software tools or Excel sheets does your team currently juggle?'\n"
        "Most prospects use 3 to 5 separate tools: Excel for stock, a paper notebook for credit, QuickBooks "
        "or a local accountant for taxes, and WhatsApp to coordinate orders. That fragmentation is their 'Silo Tax'—it "
        "wastes hours of manager time and allows inventory shrinkage. Position Bina ERP as the single source of truth."
    )

    # =========================================================================
    # SLIDE 3: THE 30,000-FOOT MODULE ECOSYSTEM MAP
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_BG_LIGHT)
    add_header(s3, "The Bina ERP Architecture: 5 Connected Business Pillars", "System Overview")

    pillars = [
        ("REVENUE & COMMERCE", C_REV, C_REV_LIGHT, [
            "CRM & Lead Intake",
            "Sales & Tax Invoicing",
            "Point of Sale (POS)",
            "Online Storefronts",
            "Customer Support Desk"
        ]),
        ("OPERATIONS & SUPPLY", C_OPS, C_OPS_LIGHT, [
            "Inventory & Stock Control",
            "Multi-Warehouse & Branches",
            "Procurement & Suppliers",
            "Manufacturing & BOMs",
            "Asset Lifecycle Management"
        ]),
        ("PEOPLE & WORK", C_HR, C_HR_LIGHT, [
            "Employee HR Directory",
            "Biometric Attendance",
            "Leave Management",
            "Automated Payroll (Tax/Pen)",
            "Projects & Billable Tasks"
        ]),
        ("FINANCE & LEDGER", C_FIN, C_FIN_LIGHT, [
            "Double-Entry Accounting",
            "Automated Journal Entries",
            "Cash Flow & Income/Expense",
            "Live Balance Sheet & P&L",
            "AR / AP Aging Reports"
        ])
    ]

    for i, (p_title, p_color, p_tint, items) in enumerate(pillars):
        px = Inches(0.8 + i * 2.98)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, Inches(1.7), Inches(2.8), Inches(4.3))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = p_color
        card.line.width = Pt(1.5)
        
        ctf = card.text_frame
        ctf.word_wrap = True
        
        # Header strip inside card
        cp = ctf.paragraphs[0]
        cp.text = p_title
        cp.font.size = Pt(11)
        cp.font.bold = True
        cp.font.color.rgb = p_color
        
        div = ctf.add_paragraph()
        div.text = "─────────────────"
        div.font.size = Pt(8)
        div.font.color.rgb = C_CARD_BORDER
        
        for item in items:
            it = ctf.add_paragraph()
            it.text = f"• {item}"
            it.font.size = Pt(10)
            it.font.color.rgb = C_TEXT_DARK
            it.font.bold = True

    # Platform Foundation Bar at the bottom
    f_bar = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.85))
    f_bar.fill.solid()
    f_bar.fill.fore_color.rgb = RGBColor(15, 23, 42) # Slate 900
    f_bar.line.fill.background()
    
    ftf = f_bar.text_frame
    ftf.word_wrap = True
    fp0 = ftf.paragraphs[0]
    fp0.text = "FOUNDATION LAYER: CORE SECURITY, MULTI-TENANCY & INTEGRATIONS"
    fp0.font.size = Pt(11)
    fp0.font.bold = True
    fp0.font.color.rgb = RGBColor(56, 189, 248) # Cyan
    
    fp1 = ftf.add_paragraph()
    fp1.text = "Role-Based Access Control (RBAC)  |  Multi-Shop Branch Isolation  |  Cloud Document Vault  |  Webhooks & Bank/Payment APIs"
    fp1.font.size = Pt(9.5)
    fp1.font.color.rgb = RGBColor(226, 232, 240)

    add_notes(s3,
        "SALES PITCH SCRIPT:\n"
        "'You don't have to adopt all 5 pillars on day one. Our modular architecture allows you to start with "
        "what hurts most—say, Point of Sale and Stock Control—and turn on Accounting, Payroll, or Manufacturing "
        "as your business expands with zero migration pain. Everything is pre-wired to talk to each other.'"
    )

    # =========================================================================
    # SLIDE 4: THE GOLDEN THREAD — END-TO-END INTEGRATION IN ACTION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_BG_LIGHT)
    add_header(s4, "The Golden Thread: How 1 Transaction Flows Across 6 Modules", "Integration In Action")

    steps = [
        ("Step 1: Capture", "CRM Module", "Lead fills web intake form. Auto-creates prospect record & alerts sales rep.", C_REV),
        ("Step 2: Close", "Sales Module", "Rep converts deal to official Tax Invoice with 15% VAT and company TIN.", C_REV),
        ("Step 3: Deduct", "Inventory", "Real-time stock decreases instantly. Warehouse alerted for packaging.", C_OPS),
        ("Step 4: Ledger", "Accounting", "Automated double-entry journal entry: debits Accounts Receivable, credits Revenue.", C_FIN),
        ("Step 5: Collect", "Finance / POS", "Customer pays via Telebirr or Cash. Cash account credited, AR cleared.", C_FIN),
        ("Step 6: Support", "Helpdesk Desk", "Customer support sees complete purchase history & warranty with 1 click.", C_PRIMARY)
    ]

    for i, (st_name, st_mod, st_desc, st_color) in enumerate(steps):
        col = i % 3
        row = i // 3
        sx = Inches(0.8 + col * 3.98)
        sy = Inches(1.7 + row * 2.6)
        
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, sy, Inches(3.7), Inches(2.35))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = st_color
        card.line.width = Pt(1.5)
        
        ctf = card.text_frame
        ctf.word_wrap = True
        
        p_num = ctf.paragraphs[0]
        p_num.text = st_name
        p_num.font.size = Pt(12)
        p_num.font.bold = True
        p_num.font.color.rgb = st_color
        
        p_mod = ctf.add_paragraph()
        p_mod.text = f"Module: {st_mod}"
        p_mod.font.size = Pt(10)
        p_mod.font.bold = True
        p_mod.font.color.rgb = C_TEXT_DARK
        
        p_desc = ctf.add_paragraph()
        p_desc.text = st_desc
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = C_TEXT_MUTED

    add_notes(s4,
        "NON-TECHNICAL TALKING SCRIPT:\n"
        "'Notice what just happened here: from the moment a customer entered their info on the website to the "
        "moment their payment hit the bank and their warranty was logged, nobody had to retype a single number. "
        "No email attachments, no WhatsApp screenshots to the warehouse, and no messy accountant reconciliation at "
        "midnight. That is the power of true integration.'"
    )

    # =========================================================================
    # REUSABLE MODULE DEEP DIVE TEMPLATE FUNCTION
    # =========================================================================
    def build_module_slide(title, category, pill_color, icon_name, what_is_it, features, integrations, why_buy, notes_text):
        sl = prs.slides.add_slide(blank_layout)
        set_slide_background(sl, C_BG_LIGHT)
        add_header(sl, title, category)

        # Left Column: What It Does & 3 Core Features (Width: 6.8 inches)
        left_card = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(6.8), Inches(5.2))
        left_card.fill.solid()
        left_card.fill.fore_color.rgb = C_CARD_BG
        left_card.line.color.rgb = C_CARD_BORDER
        left_card.line.width = Pt(1.0)
        
        ltf = left_card.text_frame
        ltf.word_wrap = True
        
        # Summary Box inside
        lp0 = ltf.paragraphs[0]
        lp0.text = "WHAT THIS MODULE DOES (IN SIMPLE TERMS)"
        lp0.font.size = Pt(11)
        lp0.font.bold = True
        lp0.font.color.rgb = pill_color
        
        lp1 = ltf.add_paragraph()
        lp1.text = what_is_it
        lp1.font.size = Pt(10.5)
        lp1.font.color.rgb = C_TEXT_DARK
        
        lp_div = ltf.add_paragraph()
        lp_div.text = "──────────────────────────────────────────────"
        lp_div.font.size = Pt(8)
        lp_div.font.color.rgb = C_CARD_BORDER

        lp_feat_title = ltf.add_paragraph()
        lp_feat_title.text = "KEY CAPABILITIES FOR YOUR CLIENTS:"
        lp_feat_title.font.size = Pt(10.5)
        lp_feat_title.font.bold = True
        lp_feat_title.font.color.rgb = C_TEXT_DARK

        for f_name, f_desc in features:
            f_p = ltf.add_paragraph()
            f_p.text = f"• {f_name}:"
            f_p.font.size = Pt(10)
            f_p.font.bold = True
            f_p.font.color.rgb = pill_color
            
            f_d = ltf.add_paragraph()
            f_d.text = f"   {f_desc}"
            f_d.font.size = Pt(9.5)
            f_d.font.color.rgb = C_TEXT_MUTED

        # Right Column Top: Connected Modules (Width: 4.6 inches)
        conn_card = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(1.7), Inches(4.6), Inches(2.6))
        conn_card.fill.solid()
        conn_card.fill.fore_color.rgb = C_CARD_BG
        conn_card.line.color.rgb = pill_color
        conn_card.line.width = Pt(1.5)
        
        ctf = conn_card.text_frame
        ctf.word_wrap = True
        cp0 = ctf.paragraphs[0]
        cp0.text = "HOW IT INTEGRATES ACROSS BINA ERP"
        cp0.font.size = Pt(11)
        cp0.font.bold = True
        cp0.font.color.rgb = pill_color
        
        for dep_mod, how_it_talks in integrations:
            ip = ctf.add_paragraph()
            ip.text = f"⇄ {dep_mod}:"
            ip.font.size = Pt(9.5)
            ip.font.bold = True
            ip.font.color.rgb = C_TEXT_DARK
            
            ip_d = ctf.add_paragraph()
            ip_d.text = f"   {how_it_talks}"
            ip_d.font.size = Pt(9)
            ip_d.font.color.rgb = C_TEXT_MUTED

        # Right Column Bottom: Why Customers Buy (Sales Pitch Card)
        why_card = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(4.5), Inches(4.6), Inches(2.4))
        why_card.fill.solid()
        why_card.fill.fore_color.rgb = RGBColor(240, 253, 250) # Light mint
        why_card.line.color.rgb = C_PRIMARY
        why_card.line.width = Pt(1.2)
        
        wtf = why_card.text_frame
        wtf.word_wrap = True
        wp0 = wtf.paragraphs[0]
        wp0.text = "WHY CLIENTS BUY (SALES TALKING POINT)"
        wp0.font.size = Pt(11)
        wp0.font.bold = True
        wp0.font.color.rgb = C_PRIMARY_DARK
        
        wp1 = wtf.add_paragraph()
        wp1.text = why_buy
        wp1.font.size = Pt(10)
        wp1.font.color.rgb = C_TEXT_DARK

        add_notes(sl, notes_text)
        return sl

    # =========================================================================
    # SLIDE 5: CRM & LEAD INTAKE
    # =========================================================================
    build_module_slide(
        "CRM & Lead Intake: Filling the Pipeline with Zero Leakage",
        "Revenue & Customer Growth",
        C_REV,
        "UserCheck",
        "Captures prospects from online forms, tracks deals across visual sales stages, and logs calls, meetings, and follow-ups so no client is ever forgotten.",
        [
            ("Interactive Lead Wizards & Forms", "Embeddable forms capture inquiries directly from customer websites or social media campaigns."),
            ("Visual Kanban Deal Stages", "Drag-and-drop deals from 'Lead In' → 'Qualified' → 'Proposal Sent' → 'Won'."),
            ("Customer 360° Activity Log", "Complete history of calls, WhatsApp notes, emails, and meetings attached to each account.")
        ],
        [
            ("Sales & Invoicing", "1-click conversion: winning a deal auto-creates a draft invoice or quotation."),
            ("Customer Support", "Support reps see the original deal notes and sales context when answering tickets.")
        ],
        "Prospects waste 30% of their marketing ad spend because inquiries get lost in WhatsApp chats or personal phones. Bina CRM ensures every lead is tracked and assigned to a rep instantly.",
        "DISCOVERY QUESTION: 'When an inquiry comes into your company right now, where does it go? Does it sit on someone's personal phone where managers can't see if it was ever followed up?'"
    )

    # =========================================================================
    # SLIDE 6: SALES & TAX INVOICING
    # =========================================================================
    build_module_slide(
        "Sales & Invoicing: Compliant Billing & Faster Cash Collection",
        "Revenue & Finance",
        C_REV,
        "FileText",
        "Creates official tax invoices, quotations, and recurring bills. Tracks client credit terms, overdue payments, and generates professional printable receipts.",
        [
            ("100% Tax & TIN Compliance", "Prints official Ethiopian Tax Invoices with legal company TIN, 15% VAT breakdown, and custom headers."),
            ("Customer Credit Limits & Terms", "Enforces maximum credit thresholds (e.g. 30-day payment terms) before blocking new orders."),
            ("Instant PDF & Auto-Receipts", "Generates clean branded PDFs that can be emailed or printed instantly upon checkout.")
        ],
        [
            ("Inventory & Warehouses", "Validating an invoice instantly reserves and subtracts items from warehouse stock."),
            ("General Ledger Accounting", "Automatically credits Sales Revenue and debits Accounts Receivable or Cash."),
            ("Finance & Cash Flow", "Payments recorded directly flow into daily cash and bank account summaries.")
        ],
        "Eliminates invoice calculation errors, prevents clients from exceeding agreed credit terms, and saves days of manual accounting reconciliations.",
        "SALES HOOK: 'Tell business owners: you'll never have to wonder who owes you money or spend 3 days making tax invoices at month-end. Bina does it in 2 clicks.'"
    )

    # =========================================================================
    # SLIDE 7: POINT OF SALE (POS)
    # =========================================================================
    build_module_slide(
        "Point of Sale (POS): High-Speed Checkout & 100% Offline Resilience",
        "Retail & Branch Operations",
        C_OPS,
        "Store",
        "A cashier register designed for speed. Fast touch screens, instant barcode beeping, cash drawer kick-outs, and shift reconciliation.",
        [
            ("100% Offline Mode", "Wi-Fi died? Store internet down? Cashiers keep ringing up sales and printing receipts. Zero downtime."),
            ("Multi-Counter & Multi-Branch", "Supports unlimited simultaneous cashier lanes (Bole, Kazanchis, Hawassa) with individual shift floats."),
            ("Thermal Receipt Integration", "Plug-and-play with standard 58mm and 80mm thermal receipt printers and 2D barcode scanners.")
        ],
        [
            ("Inventory & Stock Control", "Every barcode beep subtracts live stock. Cashiers cannot sell items that are out of stock."),
            ("Shops & Locations", "Isolates cashier sessions to specific store branches and cash drawer vaults."),
            ("Accounting & Finance", "Closing a cashier shift automatically creates a daily closing sales journal.")
        ],
        "Cashiers learn it in 15 minutes. It stops cash drawer discrepancies, cuts checkout lines in half, and never stops working when the internet cuts out.",
        "DEMO TIP: In the demo, disconnect your laptop Wi-Fi and show that POS keeps ringing up sales and prints receipts. Prospects are blown away by this reliability."
    )

    # =========================================================================
    # SLIDE 8: MULTI-STOREFRONT ECOMMERCE
    # =========================================================================
    build_module_slide(
        "Multi-Storefront E-Commerce: Selling Online 24/7 with Live Stock",
        "Omnichannel Revenue",
        C_REV,
        "ShoppingBag",
        "Launch public online web stores with custom branding. Customers browse products, place orders, and choose delivery, directly tied to the central ERP.",
        [
            ("Unified Product Master Catalog", "Upload a product picture, description, and price once—it updates your online shop and retail POS simultaneously."),
            ("Online Cart & Checkout", "Smooth customer ordering experience for retail or wholesale B2B buyers."),
            ("Multi-Channel Channel Sync", "Run distinct online stores (e.g. retail vs. wholesale) from a single shared inventory engine.")
        ],
        [
            ("Inventory Module", "Prevents overselling: an item bought in the physical shop immediately decreases web availability."),
            ("Sales & Orders", "Online purchases drop directly into the Sales Order queue for warehouse fulfillment."),
            ("Payment Gateways", "Connects to Telebirr, Chapa, CBE, or Stripe via the Integrations module.")
        ],
        "Traditional stores lose sales when their physical doors close at night. Bina E-Commerce opens a digital branch that sells 24/7 without creating messy duplicate stock.",
        "PITCH ANGLE: 'Why pay for Shopify AND an ERP that don't talk to each other? With Bina, your online store and your physical branches share the exact same database.'"
    )

    # =========================================================================
    # SLIDE 9: CUSTOMER SUPPORT & HELPDESK
    # =========================================================================
    build_module_slide(
        "Customer Support & Helpdesk: Protecting Client Retention",
        "Customer Experience",
        C_PRIMARY,
        "LifeBuoy",
        "A centralized ticketing desk for customer issues, warranties, inquiries, and a self-service knowledge base to answer common questions.",
        [
            ("Centralized Support Queue", "Organizes customer tickets by priority, department, and assigned agent with SLA response timers."),
            ("Customer Purchase Context", "Support agents can see the customer's exact invoice history and purchased serial numbers on the same screen."),
            ("Self-Service Knowledge Base", "Host product FAQs, manuals, and troubleshooting guides to resolve questions automatically.")
        ],
        [
            ("CRM Contacts", "Tickets attach directly to customer profiles for a complete 360-degree view."),
            ("Sales & Invoices", "Agents can reference original purchase dates and serial numbers for warranty claims.")
        ],
        "Acquiring a new customer costs 5x more than keeping an existing one. Helpdesk ensures customer complaints are resolved quickly with full purchase context.",
        "SALES TALKING POINT: 'When your customer calls with an issue, your support rep won't say 'Hold on while I check another system.' They see the invoice, the product serial, and the warranty status immediately.'"
    )

    # =========================================================================
    # SLIDE 10: INVENTORY & STOCK CONTROL
    # =========================================================================
    build_module_slide(
        "Inventory & Stock Control: Eliminating Shrinkage & Stockouts",
        "Core Operations",
        C_OPS,
        "Package",
        "The beating heart of supply operations. Real-time stock counts across warehouses, automatic low-stock alerts, lot tracking, and automated valuation.",
        [
            ("Multi-Warehouse & Shop Tracking", "See exact quantities on hand across all branches, warehouses, and storage bins in real time."),
            ("Automated Low-Stock Alerts", "Notifies purchasing managers before high-demand items run out of stock."),
            ("Lot & Serial Number Tracking", "Track specific batch numbers, expiration dates, and warranty serial numbers for high-value goods.")
        ],
        [
            ("Sales & POS", "Every sale at the counter or invoice created automatically deducts inventory in real time."),
            ("Procurement", "Low-stock triggers directly feed purchase order generation for restocking."),
            ("Accounting", "Maintains real-time asset balance of inventory value (FIFO / Weighted Average).")
        ],
        "Inventory shrinkage and unexpected stockouts kill retail and wholesale profits. Bina stops theft, prevents stockouts, and shows owners their exact asset valuation.",
        "DISCOVERY QUESTION: 'How do you know right now if someone in your warehouse walked out with a box of products, or if you have enough stock to fulfill tomorrow's orders?'"
    )

    # =========================================================================
    # SLIDE 11: WAREHOUSE & BRANCH LOGISTICS
    # =========================================================================
    build_module_slide(
        "Warehouse & Logistics: Disciplined Movement Between Branches",
        "Supply Chain Operations",
        C_OPS,
        "Truck",
        "Manages warehouse bins, stock transfers between branches (e.g. Central Warehouse to Bole Shop), and Goods Received verification notes.",
        [
            ("Inter-Branch Stock Transfers", "Formal transfer requests, in-transit tracking, and digital receipt sign-off prevent items 'disappearing' in transit."),
            ("Warehouse Bins & Locations", "Map items to exact aisles, shelves, and bins for rapid pick-and-pack fulfillment."),
            ("Goods Received Notes (GRN)", "Warehouse verifies incoming shipments against original purchase orders before approving stock intake.")
        ],
        [
            ("Shops Module", "Manages the stock pipeline from central distribution hubs to retail storefronts."),
            ("Procurement", "Compares vendor delivery quantities against what was actually ordered (prevents supplier under-delivery)."),
            ("Inventory", "Updates physical location tags and stock movements across multi-site facilities.")
        ],
        "Eliminates finger-pointing between branch managers and warehouse staff. Every item that moves between locations requires a digital handover signature.",
        "KEY BENEFIT: 'No more arguing over whether the Bole branch received 50 laptops or 45 laptops. Both sides must sign off digitally inside Bina.'"
    )

    # =========================================================================
    # SLIDE 12: PROCUREMENT & PURCHASING
    # =========================================================================
    build_module_slide(
        "Procurement & Purchasing: Controlling Supplier Spend",
        "Operations & Finance",
        C_OPS,
        "Truck",
        "Automates the buying workflow from Purchase Requisition → Approved Purchase Order → Vendor Delivery → Supplier Bill Payment.",
        [
            ("Purchase Orders & Approvals", "Enforces managerial approval limits before staff can commit company money to suppliers."),
            ("Supplier Directory & Pricing History", "Compares vendor prices and lead times to ensure you are always buying at the best terms."),
            ("3-Way Matching", "Matches Purchase Order + Goods Received Note + Vendor Invoice to prevent overpaying.")
        ],
        [
            ("Inventory", "Automatically updates stock levels the moment goods are received at the loading dock."),
            ("Accounting", "Creates Accounts Payable records and tracks supplier credit terms (e.g. Net 30)."),
            ("Finance", "Schedules cash disbursements to suppliers to protect company cash flow.")
        ],
        "Prevents rogue spending, duplicate supplier invoices, and ensures the company never pays for damaged or unreceived inventory.",
        "SALES PITCH: 'Tell the CFO: Bina Procurement guarantees that your company never pays a supplier invoice unless the warehouse confirms the goods arrived in good condition.'"
    )

    # =========================================================================
    # SLIDE 13: MANUFACTURING & PRODUCTION
    # =========================================================================
    build_module_slide(
        "Manufacturing & Production: Accurate Recipes & Cost of Goods",
        "Industrial & Assembly Operations",
        C_OPS,
        "Factory",
        "Transforms raw materials into finished goods. Manages multi-level Bills of Materials (BOMs), production Work Orders, and calculates true production costs.",
        [
            ("Bill of Materials (BOM Recipes)", "Define exact recipes: e.g., 1 Box of Finished Coffee = 1kg Beans + 1 Foil Bag + 1 Label."),
            ("Production Work Orders", "Schedule production runs, assign floor workers, and track manufacturing progress in real time."),
            ("Scrap & Yield Costing", "Tracks wasted raw materials and automatically factors labor and overhead into finished product cost.")
        ],
        [
            ("Inventory", "Automatically deducts raw materials and adds finished items to saleable inventory upon work order completion."),
            ("Procurement", "Identifies raw material shortages and triggers supplier orders before production halts."),
            ("Accounting", "Transfers Raw Materials Inventory value into Finished Goods Inventory on the balance sheet.")
        ],
        "Manufacturers often guess their true production costs. Bina tracks every gram of raw material and labor minute so you know your exact gross profit margin.",
        "TARGET AUDIENCE: Food & beverage packagers, furniture makers, apparel manufacturers, assembly plants, and bakeries."
    )

    # =========================================================================
    # SLIDE 14: HUMAN RESOURCES & ATTENDANCE
    # =========================================================================
    build_module_slide(
        "Human Resources (HR): Complete People & Attendance Management",
        "Human Capital Management",
        C_HR,
        "Users",
        "Digital employee files, company org charts, biometric/device clock-in attendance logs, and paperless leave request workflows.",
        [
            ("Central Employee Directory", "Contracts, emergency contacts, job descriptions, and salary structures safely stored in one cloud portal."),
            ("Daily Attendance & Clock-In", "Tracks daily check-ins, late arrivals, and absences across all branches."),
            ("Self-Service Leave Management", "Employees request annual, sick, or maternity leave from their phone; managers approve in 1 click.")
        ],
        [
            ("Payroll Module", "Feeds verified work days, overtime hours, and unpaid leave deductions directly into salary runs."),
            ("Projects", "Assigns available employees to project task boards based on department skills."),
            ("Core RBAC", "Ensures staff only see what their job allows (cashiers cannot see HR salary records).")
        ],
        "Replaces messy paper leave letters, punch cards, and WhatsApp excuse messages with an orderly, auditable HR record.",
        "SALES TALKING POINT: 'Managers spend hours every month calculating who took leave or came late. In Bina, leave balances are updated automatically, with zero dispute.'"
    )

    # =========================================================================
    # SLIDE 15: AUTOMATED PAYROLL RUNS
    # =========================================================================
    build_module_slide(
        "Payroll Runs & Payslips: 1-Click Monthly Salary Compliance",
        "People & Finance",
        C_HR,
        "Banknote",
        "Automates monthly salary calculations, income tax withholding brackets, employee pension (7%), employer pension (11%), and produces printable payslips.",
        [
            ("Built-In Ethiopian Tax Brackets", "Automatically calculates standard progressive income tax brackets—zero manual math errors."),
            ("Statutory Pension Calculations", "Accurately splits 7% employee pension and 11% company contribution with monthly reports."),
            ("1-Click PDF Payslips & Bank Schedules", "Generate individual payslips for all staff and a clean bank transfer list in seconds.")
        ],
        [
            ("HR Module", "Pulls employee salary rates, attendance summaries, and approved leave deductions automatically."),
            ("Accounting", "Posts payroll expense entries, tax liabilities, and pension payable to the General Ledger."),
            ("Finance", "Logs the net bank disbursement out of company cash accounts.")
        ],
        "Payroll that used to take 3 full days of stressful spreadsheet calculations is completed in under 5 minutes with zero tax calculation mistakes.",
        "SALES HOOK: 'Ask their HR or Finance manager: How long does payroll take you at the end of each month? When they say 2-3 days, tell them: 'In Bina, you click one button and it's done.''"
    )

    # =========================================================================
    # SLIDE 16: PROJECTS & BILLABLE TIME
    # =========================================================================
    build_module_slide(
        "Projects & Billable Time: Delivering On Time & On Budget",
        "Professional Services & Operations",
        C_OPS,
        "FolderKanban",
        "Visual Kanban boards, milestones, timesheets, and billable hour tracking for consulting firms, agencies, contractors, and project teams.",
        [
            ("Kanban Task Boards", "Organize deliverables into 'To Do', 'In Progress', 'Review', and 'Done' with deadlines and assignees."),
            ("Timesheets & Time Logging", "Team members log exact hours worked against specific client milestones and billable tasks."),
            ("Budget vs. Actual Costing", "Compare estimated hours and expenses against actual logged work to prevent project overruns.")
        ],
        [
            ("Sales & Invoicing", "Convert approved billable hours into client tax invoices with a single click."),
            ("HR", "Track employee utilization and workload distribution across concurrent client projects."),
            ("Finance", "Monitor project expenses and profitability in real time.")
        ],
        "Stop giving away free hours. Ensures every hour your team works on a client project is tracked and billed accurately.",
        "TARGET AUDIENCE: Consulting agencies, software developers, construction managers, marketing agencies, and professional services."
    )

    # =========================================================================
    # SLIDE 17: DOUBLE-ENTRY ACCOUNTING & FINANCE
    # =========================================================================
    build_module_slide(
        "Double-Entry Accounting: Automated General Ledger & Financial Statements",
        "Financial Engine",
        C_FIN,
        "BookOpen",
        "Enterprise-grade chart of accounts, automated journal entries, real-time Profit & Loss, Balance Sheets, Trial Balances, and AR/AP aging.",
        [
            ("Automated Journal Entries", "Sales, purchases, POS shifts, and payroll automatically create balanced debits & credits in the background."),
            ("Live Profit & Loss & Balance Sheet", "Know your exact net profit, gross margins, and balance sheet status today—not 30 days from now."),
            ("AR / AP Aging Dashboards", "Visual breakdowns of who owes you money (Accounts Receivable) and who you owe (Accounts Payable).")
        ],
        [
            ("The Central Hub", "Connects to Sales, POS, Procurement, Payroll, Fixed Assets, and Inventory."),
            ("Zero Double-Entry", "Accountants don't re-type cashier receipts or supplier bills; they simply review and audit.")
        ],
        "Gives business owners complete financial clarity. No waiting for external accountants. Bank-ready financial statements available 24/7.",
        "SALES SCRIPT: 'With traditional software, your books are weeks behind. With Bina, every time a cashier sells an item or a supplier bill is paid, your P&L updates instantly.'"
    )

    # =========================================================================
    # SLIDE 18: FIXED ASSETS, DOCUMENTS & CORE SECURITY
    # =========================================================================
    build_module_slide(
        "Fixed Assets, Document Vault & Core RBAC: Enterprise Control",
        "Administration & Governance",
        C_PRIMARY,
        "ShieldCheck",
        "Asset depreciation schedules, central document repository, multi-tenant isolation, and granular role-based permissions (RBAC).",
        [
            ("Automated Asset Depreciation", "Register vehicles, machinery, and IT equipment. Calculates straight-line or declining depreciation monthly."),
            ("Central Cloud Document Vault", "Attach contracts, licenses, and receipts directly to transactions, employees, or supplier files."),
            ("Granular Role Permissions (RBAC)", "Lock down sensitive data: cashiers can't see profits, sales reps can't view payroll, managers have approval limits.")
        ],
        [
            ("Accounting", "Monthly asset depreciation entries automatically update asset values and depreciation expense."),
            ("All Modules", "Document attachments and role security govern every corner of the platform.")
        ],
        "Protects company secrets, prevents fraud by rogue employees, and automates asset tax write-offs for tax audits.",
        "PEACE OF MIND POINT: 'Business owners love knowing their staff can only see what they need to see. You can customize permissions for every single employee.'"
    )

    # =========================================================================
    # SLIDE 19: THE MASTER INTEGRATION MATRIX
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_background(s19, C_BG_LIGHT)
    add_header(s19, "The Master Integration Matrix: How Data Moves in Real-Time", "Connected Ecosystem")

    # Table layout for integration matrix
    rows = 7
    cols = 4
    left = Inches(0.8)
    top = Inches(1.7)
    width = Inches(11.733)
    height = Inches(5.2)

    table_shape = s19.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # Column Widths
    table.columns[0].width = Inches(2.2) # Module
    table.columns[1].width = Inches(3.2) # Feeds Data Into
    table.columns[2].width = Inches(3.2) # Receives Data From
    table.columns[3].width = Inches(3.133) # Real-Time Trigger

    headers = ["ERP Module", "Feeds Data Directly Into", "Receives Data Directly From", "Primary Automated Trigger"]
    for j, h_text in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_PRIMARY_DARK
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_LIGHT

    matrix_data = [
        ("Point of Sale (POS)", "Inventory (Stock-out)\nAccounting (Cash/Sales)\nShops (Session Total)", "Inventory (Catalog & Barcodes)\nShops (Terminal Allocation)", "Cashier rings up item or closes daily shift session"),
        ("Sales & Invoicing", "Inventory (Stock Deduction)\nAccounting (AR / Revenue)\nFinance (Payments)", "CRM (Won Deals)\nProjects (Billable Hours)\nInventory (Price/Stock)", "Quotation approved or Tax Invoice generated"),
        ("Inventory & Stock", "Sales & POS (Availability)\nProcurement (Reorders)\nAccounting (Asset Value)", "Procurement (Goods Received)\nManufacturing (Finished Goods)\nWarehouses (Transfers)", "Barcode scanned, transfer approved, or stock count adjusted"),
        ("Procurement", "Warehouse (GRN Verification)\nInventory (Stock Increase)\nAccounting (AP / Bills)", "Inventory (Low-stock triggers)\nSuppliers (Price quotes)", "Manager approves PO or warehouse confirms delivery"),
        ("Manufacturing", "Inventory (Deducts Raw Items)\nWarehouse (Adds Finished)\nAccounting (WIP & COGS)", "Inventory (BOM components)\nProcurement (Raw materials)", "Production work order started and finished"),
        ("Payroll", "Accounting (Salaries Expense)\nFinance (Bank Disbursement)\nHR (Updated Payslips)", "HR Attendance (Hours worked)\nHR Leave (Unpaid leave)\nCore (Tax tables)", "Monthly payroll run calculated and approved")
    ]

    for i, row_data in enumerate(matrix_data):
        for j, val in enumerate(row_data):
            cell = table.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD_BG if (i % 2 == 0) else RGBColor(241, 245, 249)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            if j == 0:
                p.font.bold = True
                p.font.color.rgb = C_PRIMARY_DARK
            else:
                p.font.color.rgb = C_TEXT_DARK

    add_notes(s19,
        "MATRIX EXPLANATION FOR SALES:\n"
        "Use this slide when speaking to technical buyers, IT directors, or CFOs who ask: 'How exactly do your "
        "modules communicate?' Show them that data flows organically based on real business actions (a cashier "
        "ringing up an item, a manager approving a PO). There are no overnight batch files or manual exports."
    )

    # =========================================================================
    # SLIDE 20: 3 REAL-WORLD CUSTOMER SCENARIOS
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    set_slide_background(s20, C_BG_LIGHT)
    add_header(s20, "Target Personas: 3 Winning Sales Scenarios & Module Combos", "How to Pitch by Industry")

    scenarios = [
        ("SCENARIO 1: RETAIL & SUPERMARKET CHAINS", C_OPS, [
            "Best Fit: Supermarkets, fashion boutiques, mini-markets, hardware stores.",
            "Core Modules: POS + Inventory + Shops + Accounting + Finance.",
            "Biggest Pain: Cashier theft, long lines, stockouts during rushes.",
            "Pitch: 100% offline checkout, real-time multi-branch stock sync, and automated daily cash drawer closing summaries."
        ]),
        ("SCENARIO 2: WHOLESALE & DISTRIBUTION", C_REV, [
            "Best Fit: Importers, FMCG distributors, building material suppliers.",
            "Core Modules: CRM + Sales Invoicing + Procurement + Warehouse + AR/AP.",
            "Biggest Pain: Slow order dispatching, uncollected client debts, supplier overbilling.",
            "Pitch: Official 15% VAT invoices, strict credit terms enforcement, 3-way matching on supplier POs, and live AR aging."
        ]),
        ("SCENARIO 3: SERVICES & PROJECT AGENCIES", C_FIN, [
            "Best Fit: Consulting firms, IT companies, contractors, marketing agencies.",
            "Core Modules: CRM + Projects + Timesheets + HR + Sales Invoicing.",
            "Biggest Pain: Unbilled client hours, project cost overruns, messy payroll.",
            "Pitch: Convert staff logged timesheet hours into tax invoices in 1 click, track project budgets, and run 5-minute payroll."
        ])
    ]

    for i, (title, color, bullets) in enumerate(scenarios):
        card = s20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7 + i * 1.75), Inches(11.733), Inches(1.6))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)
        
        ctf = card.text_frame
        ctf.word_wrap = True
        
        cp0 = ctf.paragraphs[0]
        cp0.text = title
        cp0.font.size = Pt(12)
        cp0.font.bold = True
        cp0.font.color.rgb = color
        
        for b in bullets:
            bp = ctf.add_paragraph()
            bp.text = f"• {b}"
            bp.font.size = Pt(9.5)
            bp.font.color.rgb = C_TEXT_DARK

    add_notes(s20,
        "SALES STRATEGY:\n"
        "Never pitch the whole ERP blindly. First qualify which scenario the prospect belongs to: "
        "Retail, Wholesale, or Services. Then focus 80% of your presentation on their specific scenario and "
        "the 4-5 modules that solve their immediate headaches."
    )

    # =========================================================================
    # SLIDE 21: PRICING, TIERS & VALUE SELLING
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    set_slide_background(s21, C_BG_LIGHT)
    add_header(s21, "Packaging & Pricing: How to Position the 3 Tiers", "Commercial Strategy")

    tiers = [
        ("STARTER SHOP", "1,000 ETB / mo ($10)", "Single Retail Store", C_PRIMARY, [
            "Up to 5 Cashiers & Staff",
            "Lightning-Fast POS Register",
            "100% Offline Cashier Mode",
            "Official Receipt Printing with TIN",
            "Single Shop Inventory & Low Stock",
            "Customer Directory & Credit Terms",
            "Friendly WhatsApp & Phone Support"
        ], "Ideal for: Single-store boutiques, cafes, retail kiosks."),
        
        ("GROWTH BUSINESS", "2,500 ETB / mo ($25)", "MOST POPULAR", C_REV, [
            "Up to 25 Cashiers, Reps & Managers",
            "Multi-Counter Simultaneous Selling",
            "Multi-Branch Stock Transfers (Bole/Kazanchis)",
            "Instant Real-Time Profit & Loss Reports",
            "1-Click Automated Staff Payroll (Tax/Pen)",
            "Supplier Bills, POs & Delivery Intake",
            "Professional Tax Invoices (TIN & 15% VAT)",
            "Dedicated Onboarding & Live Training"
        ], "Ideal for: Busy stores, mini-markets, wholesale suppliers."),
        
        ("ENTERPRISE CHAIN", "5,000 ETB / mo ($50)", "Full Power Unlocked", C_FIN, [
            "Unlimited Branches, Cashiers & Warehouses",
            "Central Real-Time Mobile Dashboard",
            "Bulk Stock Transfers Across Warehouses",
            "Custom Staff RBAC Permissions",
            "Manufacturing & Product Assembly (BOM)",
            "Online Web Storefront with Live Stock",
            "Bank-Grade Private Cloud Database",
            "24/7 Priority Emergency Support"
        ], "Ideal for: Supermarket chains, distributors, manufacturers.")
    ]

    for i, (t_name, t_price, t_badge, t_color, t_perks, t_ideal) in enumerate(tiers):
        tx = Inches(0.8 + i * 3.98)
        card = s21.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tx, Inches(1.7), Inches(3.7), Inches(5.2))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = t_color
        card.line.width = Pt(1.5 if i != 1 else 2.5)
        
        ctf = card.text_frame
        ctf.word_wrap = True
        
        cp0 = ctf.paragraphs[0]
        cp0.text = t_name
        cp0.font.size = Pt(13)
        cp0.font.bold = True
        cp0.font.color.rgb = t_color
        
        cp_price = ctf.add_paragraph()
        cp_price.text = t_price
        cp_price.font.size = Pt(12)
        cp_price.font.bold = True
        cp_price.font.color.rgb = C_TEXT_DARK
        
        cp_badge = ctf.add_paragraph()
        cp_badge.text = f"[{t_badge}]"
        cp_badge.font.size = Pt(9.5)
        cp_badge.font.bold = True
        cp_badge.font.color.rgb = t_color
        
        div = ctf.add_paragraph()
        div.text = "──────────────────────"
        div.font.size = Pt(8)
        div.font.color.rgb = C_CARD_BORDER

        for perk in t_perks:
            pp = ctf.add_paragraph()
            pp.text = f"✓ {perk}"
            pp.font.size = Pt(9)
            pp.font.color.rgb = C_TEXT_DARK
            
        div2 = ctf.add_paragraph()
        div2.text = "──────────────────────"
        div2.font.size = Pt(8)
        div2.font.color.rgb = C_CARD_BORDER
        
        id_p = ctf.add_paragraph()
        id_p.text = t_ideal
        id_p.font.size = Pt(8.5)
        id_p.font.bold = True
        id_p.font.color.rgb = C_PRIMARY_DARK

    add_notes(s21,
        "PRICING SALES RULE:\n"
        "Never lead with price; lead with ROI. In our built-in ROI calculator, an average store with 12 staff "
        "wastes over 60 hours per week in manual tasks and inventory reconciliation. At typical wages, Bina saves "
        "them over 20,000 ETB every single month. At 2,500 ETB/mo for the Growth Business tier, Bina pays for itself "
        "nearly 10x over in the very first month!"
    )

    # =========================================================================
    # SLIDE 22: SALES DEMO PLAYBOOK & WINNING DISCOVERY QUESTIONS
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    set_slide_background(s22, C_BG_DARK)

    # Title on Dark Background
    dtb = s22.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(0.8))
    dtf = dtb.text_frame
    dp0 = dtf.paragraphs[0]
    dp0.text = "The Winning Sales Playbook: Discovery & Closing Checklist"
    dp0.font.size = Pt(24)
    dp0.font.bold = True
    dp0.font.color.rgb = C_TEXT_LIGHT
    
    dp1 = dtf.add_paragraph()
    dp1.text = "5 Questions to Uncover Pain, 3 Demo Rules, and How to Close the Deal Today"
    dp1.font.size = Pt(13)
    dp1.font.color.rgb = RGBColor(56, 189, 248) # Cyan

    # Box 1: 5 Discovery Questions (Left Column)
    q_card = s22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3))
    q_card.fill.solid()
    q_card.fill.fore_color.rgb = RGBColor(22, 33, 62)
    q_card.line.color.rgb = C_PRIMARY
    q_card.line.width = Pt(1.5)
    
    qtf = q_card.text_frame
    qtf.word_wrap = True
    qp0 = qtf.paragraphs[0]
    qp0.text = "5 GOLDEN DISCOVERY QUESTIONS TO ASK"
    qp0.font.size = Pt(12)
    qp0.font.bold = True
    qp0.font.color.rgb = RGBColor(56, 189, 248)

    questions = [
        ("1. Stock Accuracy", "'How do you currently know if your physical inventory matches what was sold at the end of the day?'"),
        ("2. Internet Reliability", "'What happens to your sales and checkout lines when your shop internet or Wi-Fi cuts out?'"),
        ("3. Credit Collection", "'How much money is currently owed to you by customers on credit, and how do you track overdue dates?'"),
        ("4. Owner Visibility", "'Can you check your store's live sales and daily profit from your phone right now while you are away?'"),
        ("5. Month-End Payroll", "'How many hours does your team spend calculating monthly staff income tax and pensions?'")
    ]
    for q_num, q_text in questions:
        p_q = qtf.add_paragraph()
        p_q.text = q_num
        p_q.font.size = Pt(10)
        p_q.font.bold = True
        p_q.font.color.rgb = C_TEXT_LIGHT
        p_a = qtf.add_paragraph()
        p_a.text = f"   {q_text}"
        p_a.font.size = Pt(9.5)
        p_a.font.color.rgb = RGBColor(203, 213, 225)

    # Box 2: 3 Demo Rules & Next Steps (Right Column)
    d_card = s22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.3))
    d_card.fill.solid()
    d_card.fill.fore_color.rgb = RGBColor(22, 33, 62)
    d_card.line.color.rgb = C_REV
    d_card.line.width = Pt(1.5)
    
    dtf_r = d_card.text_frame
    dtf_r.word_wrap = True
    dp0_r = dtf_r.paragraphs[0]
    dp0_r.text = "THE 3 GOLDEN RULES FOR LIVE DEMOS"
    dp0_r.font.size = Pt(12)
    dp0_r.font.bold = True
    dp0_r.font.color.rgb = C_REV

    rules = [
        ("Rule #1: Show the Result First", "Never show settings or configuration. Start on the lightning-fast POS register or the live Profit & Loss dashboard."),
        ("Rule #2: Hand Them the Barcode Scanner", "Let the store manager or cashier scan an item themselves. When they see how fast it beeps, they are sold."),
        ("Rule #3: Demonstrate the Offline Magic", "Disconnect the internet during the demo and ring up a receipt. Show that Bina never stops working.")
    ]
    for r_title, r_desc in rules:
        pr_t = dtf_r.add_paragraph()
        pr_t.text = f"★ {r_title}"
        pr_t.font.size = Pt(10)
        pr_t.font.bold = True
        pr_t.font.color.rgb = C_TEXT_LIGHT
        pr_d = dtf_r.add_paragraph()
        pr_d.text = f"   {r_desc}"
        pr_d.font.size = Pt(9.5)
        pr_d.font.color.rgb = RGBColor(203, 213, 225)

    div_r = dtf_r.add_paragraph()
    div_r.text = "─────────────────────────────────────────"
    div_r.font.size = Pt(8)
    div_r.font.color.rgb = RGBColor(71, 85, 105)

    cl_p = dtf_r.add_paragraph()
    cl_p.text = "HOW TO CLOSE THE MEETING:"
    cl_p.font.size = Pt(10.5)
    cl_p.font.bold = True
    cl_p.font.color.rgb = RGBColor(56, 189, 248)

    cl_call = dtf_r.add_paragraph()
    cl_call.text = "'Let's set up your store branch with a 14-day free trial right now. We can import your product spreadsheet in 10 minutes and test your first receipt.'"
    cl_call.font.size = Pt(10)
    cl_call.font.italic = True
    cl_call.font.color.rgb = C_TEXT_LIGHT

    add_notes(s22,
        "FINAL CLOSING WORDS:\n"
        "Remember, team: customers don't buy ERP software because of databases or APIs. They buy peace of mind. "
        "They buy not having their stock stolen. They buy knowing their cash is accounted for. And they buy "
        "saving 20+ hours of paperwork every week. Go out there with confidence—Bina ERP is the easiest, most "
        "reliable, and most comprehensive cloud platform built for their growth."
    )

    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_presentation()
