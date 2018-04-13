import json


def get_ticket_status(ticket_id):
    response = ""
    with open('tickets.json') as json_data:
        data = json.load(json_data)
        res = data.get('data')
        tickets = res.get('tickets')
        for ticket in tickets:
            if ticket.get('id') == int(ticket_id):
                priority_name = ticket.get('priorityName')
                customer_name = ticket.get('customerName')
                customer_id = ticket.get('customerId')
                assigned_to = ticket.get('assignedTo')
                status = ticket.get('status')
                response = 'These are the ticket details <br> <b>Customer Name:</b> {}. <br><b>Customer ID:</b> {}. <br><b>Priority:</b> {}. <br><b> Assigned To:</b> {}. <br><b> Status:</b> {}.'.format(customer_name, customer_id, priority_name, assigned_to, status)
                break
            else:
                response = "None"
        return response


def get_customer_details(customer_id):
    response = ""
    with open('customer.json') as json_data:
        customers = json.load(json_data)
        for customer in customers:
            if customer_id == customer.get("_id"):
                name = customer.get('name')
                phone = customer.get('phone')
                email = customer.get('email')
                address = customer.get('address')
                response = "These are the customer details <br><b>Name</b>: {}. <br><b>Phone:</b> {}. <br><b>Email:</b> {}. <br><b>Address:</b> {}.".format(name, phone, email, address)
                break
            else:
                response = "None"
    return response


def get_order_details(order_id):
    with open('orders.json') as json_data:
        res = json.load(json_data)
        data = res.get('data')
        partner_order_details = data.get('partner_order_details')
        order_detail = partner_order_details[0].get('orderDetail')
        if int(order_id) == partner_order_details[0].get('orderId'):
            response = "The customer has ordered the following"
            for orders in order_detail:
                response += " <br>\n <b>" + orders.get('name') + ":</b> " + str(orders.get('quantity'))
        else:
            response = "The order id does not exist."
        return response


if __name__ == '__main__':
    print(get_order_details("14"))
