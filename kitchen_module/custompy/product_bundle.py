import frappe

@frappe.whitelist()
def update_valuation_rate(docname):
    doc = frappe.get_doc('Product Bundle', docname)
    total = 0.0
    for item in doc.items:
        if item.item_code:
            bom_list = frappe.get_list("Bin", filters={"item_code": item.item_code}, fields=["name", "actual_qty", "stock_value"])
            total_actual_qty = 0.0
            total_stock_value = 0.0
            for bom in bom_list:
                total_actual_qty += bom.actual_qty
                total_stock_value += bom.stock_value
                

            item_valuation_rate = total_stock_value / total_actual_qty
            item.rate = item_valuation_rate
            item.amount = item.qty * item_valuation_rate

        total += item.amount
        doc.total = total    
    doc.save(ignore_permissions=True)
    frappe.msgprint('Valuation Rate updated successfully for all items')