# Copyright (c) 2022, SMB and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint
from frappe.model.document import Document

class MealProcess(Document):
	def before_save(self):
			if self.get_items_from == "Sales Order":
				for i in self.main_items:
					cost = 0
					for k in self.bom_list:
						if i.item_code == k.main_item and i.seles_order_ref == j.sales_order_ref:
							main_bom_qty = k.qty
						for j in self.recipe_items:
							if i.item_code == j.parent_item and i.seles_order_ref == j.sales_order_ref:
								if i.qty > 0:
									j.qty = (j.bom_qty * i.qty)/main_bom_qty
									if j.rate:
										j.amount = j.qty * j.rate
										cost = cost + j.amount
								else:
									if j.amount:
										cost = cost + j.amount	
					i.cost = cost
					#i.profit = i.amount - i.cost
			elif self.get_items_from == "Material Request":
				for i in self.main_items:
					cost = 0
					for k in self.bom_list:
						if i.item_code == k.main_item and i.material_request_ref == k.material_request_ref:
							main_bom_qty = k.qty
						for j in self.recipe_items:
							if i.item_code == j.parent_item and i.material_request_ref == j.material_request_ref:
								if i.qty > 0:
									j.qty = (j.bom_qty * i.qty)/main_bom_qty
									if j.rate:
										j.amount = j.qty * j.rate
										cost = cost + j.amount
								else:
									if j.amount:
										cost = cost + j.amount	
					i.cost = cost
					#i.profit = i.amount - i.cost
			else:
				for i in self.main_items:
					cost = 0
					for k in self.bom_list:
						if i.item_code == k.main_item:
							main_bom_qty = k.qty
						for j in self.recipe_items:
							if i.item_code == j.parent_item:
								if i.qty > 0:
									j.qty = (j.bom_qty * i.qty)/main_bom_qty
									if j.rate:
										j.amount = j.qty * j.rate
										cost = cost + j.amount
								else:
									if j.amount:
										cost = cost + j.amount	
					i.cost = cost
					#i.profit = i.amount - i.cost

	def before_submit(self):
		if self.get_items_from == "Sales Order":
			for i in self.main_items:
				se = frappe.new_doc("Stock Entry")
				se.stock_entry_type = self.stock_entry_type
				se.meal_process = self.name
				se.set_posting_time = 1
				se.posting_date = self.posting_date
				se.from_bom = 1
				se.from_warehouse = self.source_warehouse
				se.to_warehouse = self.target_warehouse
				for j in self.bom_list:
					if i.item_code == j.main_item and i.sales_order_ref == j.sales_order_ref:
						se.bom_no = j.bom
				se.fg_completed_qty = i.qty

				for k in self.recipe_items:
					if i.item_code == k.parent_item and i.sales_order_ref == k.sales_order_ref:
						se_item = frappe.new_doc("Stock Entry Detail")
						se_item.s_warehouse = self.source_warehouse
						se_item.item_code = k.item_code
						se_item.qty = k.qty
						se_item.basic_rate = k.rate
						if i.rate == 0:
							se_item.allow_zero_valuation_rate = 1
						se.append("items", se_item)

				se_item = frappe.new_doc("Stock Entry Detail")
				se_item.t_warehouse = self.target_warehouse
				se_item.item_code = i.item_code
				se_item.is_finished_item = 1
				se_item.qty = i.qty
				se_item.basic_rate = i.cost/i.qty
				se.append("items", se_item)		

				se.save()
				se.submit() 

		elif self.get_items_from == "Material Request":	
			for i in self.main_items:
				se = frappe.new_doc("Stock Entry")
				se.stock_entry_type = self.stock_entry_type
				se.meal_process = self.name
				se.set_posting_time = 1
				se.posting_date = self.posting_date
				se.from_bom = 1
				se.from_warehouse = self.source_warehouse
				se.to_warehouse = self.target_warehouse
				for j in self.bom_list:
					if i.item_code == j.main_item and i.material_request_ref == j.material_request_ref:
						se.bom_no = j.bom
				se.fg_completed_qty = i.qty

				for k in self.recipe_items:
					if i.item_code == k.parent_item and i.material_request_ref == k.material_request_ref:
						se_item = frappe.new_doc("Stock Entry Detail")
						se_item.s_warehouse = self.source_warehouse
						se_item.item_code = k.item_code
						se_item.qty = k.qty
						se_item.basic_rate = k.rate
						if i.rate == 0:
							se_item.allow_zero_valuation_rate = 1
						se.append("items", se_item)

				se_item = frappe.new_doc("Stock Entry Detail")
				se_item.t_warehouse = self.target_warehouse
				se_item.item_code = i.item_code
				se_item.is_finished_item = 1
				se_item.qty = i.qty
				se_item.basic_rate = i.cost/i.qty
				se.append("items", se_item)		

				se.save()
				se.submit()

		elif self.get_items_from == "Bulk Upload" or self.get_items_from == "Item Group" or self.get_items_from == "":	
			for i in self.main_items:
				se = frappe.new_doc("Stock Entry")
				se.stock_entry_type = self.stock_entry_type
				se.meal_process = self.name
				se.set_posting_time = 1
				se.posting_date = self.posting_date
				se.from_bom = 1
				se.from_warehouse = self.source_warehouse
				se.to_warehouse = self.target_warehouse
				for j in self.bom_list:
					if i.item_code == j.main_item:
						se.bom_no = j.bom
				se.fg_completed_qty = i.qty

				for k in self.recipe_items:
					if i.item_code == k.parent_item:
						se_item = frappe.new_doc("Stock Entry Detail")
						se_item.s_warehouse = self.source_warehouse
						se_item.item_code = k.item_code
						se_item.qty = k.qty
						se_item.basic_rate = k.rate
						if i.rate == 0:
							se_item.allow_zero_valuation_rate = 1
						se.append("items", se_item)

				se_item = frappe.new_doc("Stock Entry Detail")
				se_item.t_warehouse = self.target_warehouse
				se_item.item_code = i.item_code
				se_item.is_finished_item = 1
				se_item.qty = i.qty
				se_item.basic_rate = i.cost/i.qty
				se.append("items", se_item)		

				se.save()
				se.submit()

	def submit(self):
		if len(self.main_items) > 5:
			msgprint(_("The task has been enqueued as a background job. In case there is any issue on processing in background, the system will add a comment about the error on this Meal Process and revert to the Draft stage"))
			self.queue_action('submit', timeout=3000)
		else:
			self._submit()

	# def before_cancel(self):
	# 	se = frappe.get_doc('Stock Entry', self.stock_entry)
	# 	se.cancel()
	# 	se.save()
	# 	self.stock_entry = ""
	# 	self.cancel_stock_entry = se.name

