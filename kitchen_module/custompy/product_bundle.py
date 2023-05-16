import frappe
from erpnext.manufacturing.doctype.bom.bom import get_valuation_rate

@frappe.whitelist()
def update_valuation_rate(docname):
    doc = frappe.get_doc('Product Bundle', docname)
    total = 0.0
    for item in doc.items:
        if item.item_code:
            if frappe.db.exists("BOM",{"item": item.item_code,"docstatus": 1,"is_active": 1,"is_default": 1}):
                filters = {
                    "item": item.item_code,
                    "docstatus": 1,
                    "is_active": 1,
                    "is_default": 1
                }
                result = frappe.get_all("BOM", filters=filters, limit=1)
                if result:
                    bom_doc = frappe.get_doc("BOM", result[0].name)
                    item_valuation_rate = ( bom_doc.total_cost * 1 ) / bom_doc.quantity
            else:    
                args = {
                    "item_code": item.item_code,
                    "company": doc.company,
                }
                item_valuation_rate = get_valuation_rate(args)

            item.rate = item_valuation_rate
            item.amount = item.qty * item_valuation_rate

        total += item.amount
        doc.total = total    
    doc.save(ignore_permissions=True)
    frappe.msgprint('Valuation Rate updated successfully for all items')