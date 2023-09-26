import os
import json
import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    # Open a WebSocket connection
    def open(self):
        print("WebSocket opened")

    # Close a WebSocket connection
    def on_close(self):
        print("WebSocket closed")

    def on_message(self, message):
        data = json.loads(message)
        command = data.get('command')
        if command == 'add':
            transaction = data.get('transaction')
            if transaction:
                self.add_transaction(transaction)
        elif command == 'delete':
            id = data.get('id')
            if id:
                self.delete_transaction(id)
        elif command == 'update':
            id = data.get('id')
            operator = data.get('operator')
            amount = data.get('amount')
            if id and operator and amount:
                self.update_transaction(id, operator, amount)
        else:
            self.write_message('Unknown command')

    def add_transaction(self, transaction):
        filename = os.environ.get('TRANSACTIONS_FILE', os.path.join(os.getcwd(), 'transactions.json'))
        transactions = []
        try:
            with open(filename, 'r') as f:
                # check if the file is empty
                if os.stat(filename).st_size == 0:
                    # if the file is empty, initialize it with an empty JSON array
                    transactions = []
                else:
                    transactions = json.load(f)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            # if the file contains invalid JSON, initialize it with an empty JSON array
            transactions = []
        
        # check if the transaction is in the correct JSON format
        if isinstance(transaction, dict):
            transactions.append(transaction)
            with open(filename, 'w') as f:
                json.dump(transactions, f)
            self.write_message('Transaction added')
        else:
            self.write_message('Invalid transaction format')

    # Delete a transaction from the transactions file
    def delete_transaction(self, id):
        filename = os.environ.get('TRANSACTIONS_FILE', os.path.join(os.getcwd(), 'transactions.json'))
        with open(filename, 'r') as f:
            transactions = json.load(f)
        found = False
        for i, transaction in enumerate(transactions):
            if transaction.get('id') == id:
                found = True
                del transactions[i]
                break
        if found:
            with open(filename, 'w') as f:
                json.dump(transactions, f)
            self.write_message('Transaction deleted')
        else:
            self.write_message('Transaction not found')

    # Update a transaction in the transactions file
    def update_transaction(self, id, operator, amount):
        filename = os.environ.get('TRANSACTIONS_FILE', os.path.join(os.getcwd(), 'transactions.json'))
        with open(filename, 'r') as f:
            transactions = json.load(f)
        found = False
        for transaction in transactions:
            if transaction.get('id') == id:
                found = True
                current_amount = transaction.get('amount')
                result = {}
                try:
                    code = compile(f'result = {int(current_amount)} {operator} {int(amount)}', '<string>', 'exec')
                    exec(code, result)
                    transaction['amount'] = result.get('result')
                    break
                except:
                    self.write_message(json.dumps({'error': 'Something Went Wrong!'}))
        if found:
            with open(filename, 'w') as f:
                json.dump(transactions, f)
            self.write_message(json.dumps({'result': f"Transaction updated: {transaction}"}))
        else:
            self.write_message('Transaction not found')

# Define a class for the main web application
class Application(tornado.web.Application):
    def __init__(self):
        # Define the application's handlers
        handlers = [
            (r'/websocket', WebSocketHandler)
        ]

        # Configure the application settings
        settings = {
            'debug': True,
            'autoreload': True
        }

        # Call the superclass initialization
        super().__init__(handlers, **settings)

# Create the application and start the server
if __name__ == '__main__':
    app = Application()
    # Start the server
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()
