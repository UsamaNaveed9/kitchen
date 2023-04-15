
frappe.ui.form.on('Product Bundle', {
    get_rate: function(frm) {
        if(frm.doc.items){
            frappe.call({
                method: 'kitchen_module.custompy.product_bundle.update_valuation_rate',
                args: {docname: frm.doc.name},
                callback: function(response) {
                    frm.reload_doc();
                }
            });
        }
        
    }
});