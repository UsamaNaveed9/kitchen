
frappe.ui.form.on('Product Bundle', {
    get_rate: function(frm) {
        if(frm.doc.items){
            frappe.call({
                method: 'kitchen_module.custompy.product_bundle.update_valuation_rate',
                args: {docname: frm.doc.name},
                callback: function(response) {
                    cur_frm.refresh();
                }
            });
        }
        
    }
});

frappe.ui.form.on('Product Bundle Item', {
    item_code: function(frm,cdt,cdn) {
        var row = locals[cdt][cdn];
        var qty = 1
        frappe.model.set_value(cdt, cdn, "qty", parseFloat(qty));

    },
    items_remove:function(frm, cdt, cdn) {
        var total = 0;
        cur_frm.doc.items.forEach(function(d) { total += d.amount; });
	    cur_frm.set_value('total', total);
	}
});