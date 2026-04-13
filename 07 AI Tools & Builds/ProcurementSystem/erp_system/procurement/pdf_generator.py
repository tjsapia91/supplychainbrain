"""
PPO PDF Generator for Michael Todd Beauty ERP System
Generates Planned Purchase Order PDFs matching the Excel PPO-3147 format.

Layout:
  - Company header with HQ address
  - "Planned Purchase Order" title
  - Left: Bill-To + Seller/Exporter  |  Right: PPO details + Ship-To (3PL)
  - Shipment info row
  - Line items table with CTNS/CBM columns
  - Totals
  - Factory wire info
  - Footer with signature line and contact info
"""

from io import BytesIO
from datetime import datetime
from decimal import Decimal
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black, lightgrey
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from django.utils.dateformat import format as django_date_format
from django.conf import settings
import os


def _fmt_date(d, fmt='m/d/Y'):
    """Format a date safely"""
    if not d:
        return ''
    return django_date_format(d, fmt)


NAVY = HexColor('#1f4788')
GOLD = HexColor('#d4a574')
LIGHT_GRAY = HexColor('#f5f5f5')
DARK_GRAY = HexColor('#666666')
MEDIUM_GRAY = HexColor('#999999')

HQ_ADDRESS = "548 NW University Blvd., Suite 600, Port St. Lucie, FL 34986"
HQ_PHONE = "1-772-446-0149"
HQ_WEB = "www.michaeltoddbeauty.com"
HQ_EMAIL = "supplychain@michaeltoddbeauty.com"


def _safe(val, default=''):
    """Safely get a string value, handling None"""
    if val is None:
        return default
    return str(val)


def generate_ppo_pdf(ppo):
    """
    Generate a PDF for a PlannedPurchaseOrder instance.
    Returns BytesIO object containing the PDF.
    """
    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.4 * inch,
        bottomMargin=0.4 * inch,
    )

    story = []

    # --- Header: PPO title + PPO number/date on the right ---
    story.append(_build_header_with_ppo_info(ppo))
    story.append(Spacer(1, 0.05 * inch))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY))
    story.append(Spacer(1, 0.15 * inch))

    # --- Two-column: Bill-To/Seller on left, PPO Details/Ship-To on right ---
    story.append(_build_addresses_and_details(ppo))
    story.append(Spacer(1, 0.15 * inch))

    # --- Shipment Information ---
    story.append(_build_shipment_info(ppo))
    story.append(Spacer(1, 0.15 * inch))

    # --- Line Items Table ---
    story.append(_build_line_items_table(ppo))
    story.append(Spacer(1, 0.1 * inch))

    # --- Totals ---
    story.append(_build_totals_section(ppo))
    story.append(Spacer(1, 0.15 * inch))

    # --- Factory Wire Info ---
    if ppo.wire_info:
        story.append(_build_wire_info(ppo))
        story.append(Spacer(1, 0.1 * inch))

    # --- Special Notes ---
    if ppo.special_notes:
        story.append(_build_special_notes(ppo))
        story.append(Spacer(1, 0.1 * inch))

    # --- Signature Line ---
    story.append(_build_signature_line(ppo))
    story.append(Spacer(1, 0.1 * inch))

    # --- Footer ---
    story.append(_build_footer())

    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer


# ===========================================================================
# SECTION BUILDERS
# ===========================================================================

def _build_header_with_ppo_info(ppo):
    """Header: 'PLANNED PURCHASE ORDER' title on the left, PPO #/date on the right"""
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'PPOTitle', parent=styles['Normal'],
        fontSize=16, fontName='Helvetica-Bold', textColor=NAVY, alignment=TA_LEFT,
        leading=20,
    )
    ppo_num_style = ParagraphStyle(
        'PPONum', parent=styles['Normal'],
        fontSize=14, fontName='Helvetica-Bold', textColor=NAVY, alignment=TA_RIGHT,
        leading=18,
    )
    date_style = ParagraphStyle(
        'DateStyle', parent=styles['Normal'],
        fontSize=9, textColor=DARK_GRAY, alignment=TA_RIGHT, leading=13,
    )

    ppo_date = ''
    if ppo.date:
        ppo_date = _fmt_date(ppo.date)

    data = [[
        Paragraph('PLANNED PURCHASE ORDER', title_style),
        Paragraph(f"{ppo.ppo_number}", ppo_num_style),
    ], [
        Paragraph('', title_style),
        Paragraph(f"Date: {ppo_date}  |  Page 1 of 1", date_style),
    ]]

    table = Table(data, colWidths=[4.5 * inch, 3 * inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    return table


def _build_addresses_and_details(ppo):
    """Two-column layout: Bill-To + Seller on left, PPO details + Ship-To on right"""
    styles = getSampleStyleSheet()

    section_label = ParagraphStyle(
        'SectionLabel', parent=styles['Normal'],
        fontSize=8, fontName='Helvetica-Bold', textColor=white,
    )
    text_style = ParagraphStyle(
        'AddrText', parent=styles['Normal'],
        fontSize=8, leading=11,
    )
    bold_text = ParagraphStyle(
        'BoldText', parent=styles['Normal'],
        fontSize=8, fontName='Helvetica-Bold', leading=11,
    )
    detail_label = ParagraphStyle(
        'DetailLabel', parent=styles['Normal'],
        fontSize=8, fontName='Helvetica-Bold', textColor=DARK_GRAY, alignment=TA_RIGHT,
    )
    detail_val = ParagraphStyle(
        'DetailVal', parent=styles['Normal'],
        fontSize=8, alignment=TA_LEFT,
    )

    # ---- LEFT COLUMN: Bill-To + Seller ----
    # Build Bill-To section — uses the PPO's branch name with shared HQ address
    bill_to_rows = []
    bill_to_rows.append([Paragraph('BILL TO:', section_label)])

    # Branch name from the PPO (Spa Sciences, NasalFresh MD, or Michael Todd Beauty)
    bill_to_name = 'Michael Todd Beauty'
    if ppo.branch:
        bill_to_name = ppo.branch.name

    bill_to_rows.append([Paragraph(f"<b>{bill_to_name}</b>", text_style)])
    bill_to_rows.append([Paragraph(HQ_ADDRESS, text_style)])
    bill_to_rows.append([Paragraph(f"Phone: {HQ_PHONE}", text_style)])
    bill_to_rows.append([Paragraph(f"Contact: {HQ_EMAIL}", text_style)])

    bill_to_table = Table(bill_to_rows, colWidths=[3.5 * inch])
    bill_to_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), NAVY),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))

    # Build Seller section
    seller_rows = []
    seller_rows.append([Paragraph('SELLER / EXPORTER:', section_label)])
    seller_rows.append([Paragraph(f"<b>{_safe(ppo.vendor.name)}</b>", text_style)])
    if ppo.vendor.address:
        seller_rows.append([Paragraph(ppo.vendor.address, text_style)])
    city_line = ''
    if ppo.vendor.city:
        city_line += ppo.vendor.city
    if ppo.vendor.state:
        city_line += f", {ppo.vendor.state}"
    if ppo.vendor.postal_code:
        city_line += f" {ppo.vendor.postal_code}"
    if city_line:
        seller_rows.append([Paragraph(city_line, text_style)])
    if ppo.vendor.country:
        seller_rows.append([Paragraph(ppo.vendor.country, text_style)])
    if ppo.vendor.phone:
        seller_rows.append([Paragraph(f"Phone: {ppo.vendor.phone}", text_style)])
    if ppo.vendor.contact_name:
        seller_rows.append([Paragraph(f"Contact: {ppo.vendor.contact_name}", text_style)])
    if ppo.vendor.contact_email:
        seller_rows.append([Paragraph(f"Email: {ppo.vendor.contact_email}", text_style)])

    seller_table = Table(seller_rows, colWidths=[3.5 * inch])
    seller_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), NAVY),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))

    # Stack Bill-To and Seller vertically on the left
    left_col = [[bill_to_table], [Spacer(1, 0.1 * inch)], [seller_table]]
    left_stack = Table(left_col, colWidths=[3.5 * inch])
    left_stack.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    # ---- RIGHT COLUMN: PPO Details + Ship-To ----
    pi_number = _safe(ppo.vendor_pi_number)
    req_ship = 'TBD'
    if ppo.requested_ship_date:
        req_ship = _fmt_date(ppo.requested_ship_date)

    details_rows = [
        [Paragraph('PO #:', detail_label), Paragraph(f"{ppo.ppo_number}", bold_text)],
        [Paragraph('Vendor PI #:', detail_label), Paragraph(pi_number, detail_val)],
        [Paragraph('Req. Ship Date:', detail_label), Paragraph(req_ship, detail_val)],
        [Paragraph('Currency:', detail_label), Paragraph(_safe(ppo.currency, 'USD'), detail_val)],
        [Paragraph('Incoterms:', detail_label), Paragraph(_safe(ppo.incoterms), detail_val)],
    ]

    details_table = Table(details_rows, colWidths=[1.5 * inch, 2.0 * inch])
    details_table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_GRAY),
        ('GRID', (0, 0), (-1, -1), 0.25, lightgrey),
    ]))

    # Ship-To section
    ship_to_rows = []
    ship_to_rows.append([Paragraph('SHIP TO:', section_label)])
    if ppo.ship_to_3pl:
        ship_to_rows.append([Paragraph(f"<b>{_safe(ppo.ship_to_3pl.name)}</b>", text_style)])
        if ppo.ship_to_3pl.address and ppo.ship_to_3pl.address.strip() and not ppo.ship_to_3pl.address.startswith('TBD'):
            ship_to_rows.append([Paragraph(ppo.ship_to_3pl.address, text_style)])
        tpl_city = ''
        if ppo.ship_to_3pl.city:
            tpl_city += ppo.ship_to_3pl.city
        if ppo.ship_to_3pl.state:
            tpl_city += f", {ppo.ship_to_3pl.state}"
        if ppo.ship_to_3pl.zip_code:
            tpl_city += f" {ppo.ship_to_3pl.zip_code}"
        if tpl_city:
            ship_to_rows.append([Paragraph(tpl_city, text_style)])
        if ppo.ship_to_3pl.contact_name:
            ship_to_rows.append([Paragraph(f"Contact: {ppo.ship_to_3pl.contact_name}", text_style)])
    else:
        ship_to_rows.append([Paragraph('', text_style)])

    ship_to_table = Table(ship_to_rows, colWidths=[3.5 * inch])
    ship_to_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), NAVY),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))

    # Stack details and ship-to vertically on the right
    right_col = [[details_table], [Spacer(1, 0.1 * inch)], [ship_to_table]]
    right_stack = Table(right_col, colWidths=[3.5 * inch])
    right_stack.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    # Combine left and right
    layout = Table([[left_stack, right_stack]], colWidths=[3.75 * inch, 3.75 * inch])
    layout.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    return layout


def _build_shipment_info(ppo):
    """Shipment information row"""
    styles = getSampleStyleSheet()

    label_style = ParagraphStyle(
        'ShipLabel', parent=styles['Normal'],
        fontSize=7, fontName='Helvetica-Bold', textColor=DARK_GRAY,
    )
    val_style = ParagraphStyle(
        'ShipVal', parent=styles['Normal'],
        fontSize=8,
    )
    header_style = ParagraphStyle(
        'ShipHeader', parent=styles['Normal'],
        fontSize=9, fontName='Helvetica-Bold', textColor=white,
    )

    req_ship = 'TBD'
    if ppo.requested_ship_date:
        req_ship = _fmt_date(ppo.requested_ship_date)
    est_ship = 'TBD'
    if ppo.estimated_ship_date:
        est_ship = _fmt_date(ppo.estimated_ship_date)
    lead_time = 'TBD'
    if ppo.lead_time_days:
        lead_time = f"{ppo.lead_time_days} days"
    transport = _safe(ppo.get_mode_of_transport_display(), ppo.mode_of_transport)

    data = [
        [Paragraph('SHIPMENT INFORMATION', header_style), '', '', '', '', ''],
        [
            Paragraph('Req. Ship Date', label_style),
            Paragraph('Est. Ship Date', label_style),
            Paragraph('Payment Terms', label_style),
            Paragraph('Mode of Transport', label_style),
            Paragraph('Lead Time', label_style),
            Paragraph('Incoterms', label_style),
        ],
        [
            Paragraph(req_ship, val_style),
            Paragraph(est_ship, val_style),
            Paragraph(_safe(ppo.payment_terms), val_style),
            Paragraph(transport, val_style),
            Paragraph(lead_time, val_style),
            Paragraph(_safe(ppo.incoterms), val_style),
        ],
        [
            Paragraph('Port of Loading', label_style),
            Paragraph('Port of Discharge', label_style),
            Paragraph('Country of Origin', label_style),
            Paragraph('AWB/BL #', label_style),
            Paragraph('Total CBM', label_style),
            Paragraph('Total Cartons', label_style),
        ],
        [
            Paragraph(_safe(ppo.port_of_loading), val_style),
            Paragraph(_safe(ppo.port_of_discharge), val_style),
            Paragraph(_safe(ppo.country_of_origin), val_style),
            Paragraph(_safe(ppo.awb_bl_number), val_style),
            Paragraph(f"{float(ppo.total_cbm or 0):.4f}", val_style),
            Paragraph(str(ppo.total_cartons or 0), val_style),
        ],
    ]

    col_w = 7.5 / 6
    table = Table(data, colWidths=[col_w * inch] * 6)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('SPAN', (0, 0), (-1, 0)),
        ('GRID', (0, 1), (-1, -1), 0.5, lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_GRAY),
        ('BACKGROUND', (0, 3), (-1, 3), LIGHT_GRAY),
    ]))
    return table


def _build_line_items_table(ppo):
    """Line items table with item #, description, qty, price, ctns, cbm, notes, destination"""
    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        'TblHeader', parent=styles['Normal'],
        fontSize=7, fontName='Helvetica-Bold', textColor=white, alignment=TA_CENTER,
    )
    text_style = ParagraphStyle(
        'TblText', parent=styles['Normal'],
        fontSize=7, alignment=TA_LEFT,
    )
    center_style = ParagraphStyle(
        'TblCenter', parent=styles['Normal'],
        fontSize=7, alignment=TA_CENTER,
    )
    right_style = ParagraphStyle(
        'TblRight', parent=styles['Normal'],
        fontSize=7, alignment=TA_RIGHT,
    )

    data = [[
        Paragraph('#', header_style),
        Paragraph('MT/SS ITEM #', header_style),
        Paragraph('DESCRIPTION', header_style),
        Paragraph('QTY', header_style),
        Paragraph('UNIT PRICE', header_style),
        Paragraph('TOTAL CTNS', header_style),
        Paragraph('CBM', header_style),
        Paragraph('NOTES', header_style),
        Paragraph('DEST.', header_style),
        Paragraph('LINE TOTAL', header_style),
    ]]

    lines = ppo.lines.all().order_by('line_number')
    for idx, line in enumerate(lines, 1):
        unit_price = ''
        if line.unit_price:
            unit_price = f"${float(line.unit_price):.2f}"
        cbm = ''
        if line.cbm:
            cbm = f"{float(line.cbm):.4f}"
        cartons = ''
        if line.cartons:
            cartons = str(line.cartons)
        line_total_str = ''
        if line.line_total:
            line_total_str = f"${float(line.line_total):.2f}"

        item_no = ''
        if line.item:
            item_no = str(line.item.item_no)

        desc = ''
        if line.description:
            desc = line.description[:60]

        notes = ''
        if line.notes:
            notes = line.notes[:40]

        dest = _safe(line.destination)

        qty_str = f"{line.quantity:,}" if line.quantity else ''

        data.append([
            Paragraph(str(idx), center_style),
            Paragraph(item_no, text_style),
            Paragraph(desc, text_style),
            Paragraph(qty_str, center_style),
            Paragraph(unit_price, right_style),
            Paragraph(cartons, center_style),
            Paragraph(cbm, right_style),
            Paragraph(notes, text_style),
            Paragraph(dest, text_style),
            Paragraph(line_total_str, right_style),
        ])

    if len(data) == 1:
        data.append([Paragraph('', text_style)] * 10)

    col_widths = [
        0.3 * inch,   # #
        0.85 * inch,  # Item #
        1.55 * inch,  # Description
        0.5 * inch,   # QTY
        0.65 * inch,  # Unit Price
        0.5 * inch,   # CTNS
        0.55 * inch,  # CBM
        0.8 * inch,   # Notes
        0.65 * inch,  # Destination
        0.75 * inch,  # Line Total
    ]

    table = Table(data, colWidths=col_widths, repeatRows=1)

    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, lightgrey),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]

    for i in range(1, len(data)):
        if i % 2 == 0:
            table_style.append(('BACKGROUND', (0, i), (-1, i), LIGHT_GRAY))

    table.setStyle(TableStyle(table_style))
    return table


def _build_totals_section(ppo):
    """Right-aligned totals section"""
    styles = getSampleStyleSheet()

    label_style = ParagraphStyle(
        'TotalLabel', parent=styles['Normal'],
        fontSize=9, fontName='Helvetica-Bold', alignment=TA_RIGHT,
    )
    total_style = ParagraphStyle(
        'TotalValue', parent=styles['Normal'],
        fontSize=9, alignment=TA_RIGHT,
    )
    grand_total_label = ParagraphStyle(
        'GrandTotalLabel', parent=styles['Normal'],
        fontSize=11, fontName='Helvetica-Bold', alignment=TA_RIGHT, textColor=white,
    )
    grand_total_val = ParagraphStyle(
        'GrandTotalVal', parent=styles['Normal'],
        fontSize=11, fontName='Helvetica-Bold', alignment=TA_RIGHT, textColor=white,
    )

    subtotal = f"${float(ppo.subtotal or 0):,.2f}"
    deposit = f"${float(ppo.deposit or 0):,.2f}"
    balance = f"${float(ppo.balance_due or 0):,.2f}"
    total = f"${float(ppo.total or 0):,.2f}"

    data = [
        ['', Paragraph('Subtotal:', label_style), Paragraph(subtotal, total_style)],
        ['', Paragraph('Deposit:', label_style), Paragraph(deposit, total_style)],
        ['', Paragraph('Balance Due:', label_style), Paragraph(balance, total_style)],
        ['', Paragraph('TOTAL:', grand_total_label), Paragraph(total, grand_total_val)],
    ]

    table = Table(data, colWidths=[4.5 * inch, 1.5 * inch, 1.5 * inch])
    table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LINEABOVE', (1, 0), (-1, 0), 0.5, lightgrey),
        ('LINEBELOW', (1, 2), (-1, 2), 0.5, lightgrey),
        ('BACKGROUND', (1, 3), (-1, 3), NAVY),
        ('TEXTCOLOR', (1, 3), (-1, 3), white),
    ]))
    return table


def _build_wire_info(ppo):
    """Factory wire/bank information section"""
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'WireTitle', parent=styles['Normal'],
        fontSize=9, fontName='Helvetica-Bold', textColor=white,
    )
    text_style = ParagraphStyle(
        'WireText', parent=styles['Normal'],
        fontSize=8, leading=11,
    )

    data = [
        [Paragraph('FACTORY WIRE INFORMATION', title_style)],
        [Paragraph(ppo.wire_info.replace('\n', '<br/>'), text_style)],
    ]

    table = Table(data, colWidths=[7.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (0, 0), white),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('BOX', (0, 0), (-1, -1), 0.5, lightgrey),
    ]))
    return table


def _build_special_notes(ppo):
    """Special notes section"""
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'NotesTitle', parent=styles['Normal'],
        fontSize=9, fontName='Helvetica-Bold', textColor=NAVY,
    )
    text_style = ParagraphStyle(
        'NotesText', parent=styles['Normal'],
        fontSize=8, leading=11,
    )

    data = [
        [Paragraph('SPECIAL NOTES:', title_style)],
        [Paragraph(ppo.special_notes.replace('\n', '<br/>'), text_style)],
    ]

    table = Table(data, colWidths=[7.5 * inch])
    table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('BOX', (0, 0), (-1, -1), 0.5, lightgrey),
    ]))
    return table


def _build_signature_line(ppo=None):
    """Signature line with declaration and CEO signature if approved"""
    styles = getSampleStyleSheet()

    decl_style = ParagraphStyle(
        'Declaration', parent=styles['Normal'],
        fontSize=7, alignment=TA_CENTER, textColor=DARK_GRAY, leading=10,
    )
    sig_style = ParagraphStyle(
        'SigLine', parent=styles['Normal'],
        fontSize=8, alignment=TA_CENTER,
    )
    typed_sig_style = ParagraphStyle(
        'TypedSig', parent=styles['Normal'],
        fontSize=18, alignment=TA_CENTER, textColor=NAVY,
        fontName='Times-Italic',
    )
    approval_info_style = ParagraphStyle(
        'ApprovalInfo', parent=styles['Normal'],
        fontSize=7, alignment=TA_CENTER, textColor=DARK_GRAY, leading=9,
    )

    data = [
        [Paragraph(
            "I declare that the information mentioned above is true and correct. "
            "This is a planned purchase order and subject to approval.",
            decl_style
        )],
        [Spacer(1, 0.15 * inch)],
    ]

    # Show actual CEO signature if the PPO is approved
    has_signature = False
    if ppo and ppo.ceo_approved_by:
        if ppo.ceo_signature_type == 'image' and ppo.ceo_signature_image:
            # Render uploaded signature image
            try:
                img_path = ppo.ceo_signature_image.path
                if os.path.exists(img_path):
                    sig_img = Image(img_path, width=2 * inch, height=0.6 * inch)
                    sig_img.hAlign = 'CENTER'
                    data.append([sig_img])
                    has_signature = True
            except Exception:
                pass
        elif ppo.ceo_signature_type == 'typed' and ppo.ceo_signature_text:
            # Render typed signature in cursive/italic
            data.append([Paragraph(ppo.ceo_signature_text, typed_sig_style)])
            has_signature = True

    if not has_signature:
        # Show blank signature line
        data.append([Spacer(1, 0.15 * inch)])

    data.append([Paragraph("_" * 50, sig_style)])

    if ppo and ppo.ceo_approved_by and ppo.ceo_approval_date:
        approval_text = (
            f"Approved by {ppo.ceo_approved_by.get_full_name() or ppo.ceo_approved_by.username}"
            f" &mdash; {_fmt_date(ppo.ceo_approval_date, 'F d, Y')}"
        )
        data.append([Paragraph(approval_text, approval_info_style)])
    else:
        data.append([Paragraph("Authorized Signature &amp; Date", decl_style)])

    table = Table(data, colWidths=[7.5 * inch])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    return table


def _build_footer():
    """Footer with company contact info"""
    styles = getSampleStyleSheet()

    footer_style = ParagraphStyle(
        'Footer', parent=styles['Normal'],
        fontSize=7, alignment=TA_CENTER, textColor=DARK_GRAY, leading=10,
    )

    text = (
        f"Should you have any question concerning this order, "
        f"please contact <b>{HQ_EMAIL}</b><br/>"
        f"<b>Michael Todd Beauty</b>  |  {HQ_ADDRESS}  |  "
        f"Tel: {HQ_PHONE}  |  {HQ_WEB}"
    )

    return Paragraph(text, footer_style)
