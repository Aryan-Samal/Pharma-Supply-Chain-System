import hashlib
import datetime

class Drug:
    def __init__(self, drug_id, name, manufacturer):
        self.drug_id = drug_id
        self.name = name
        self.manufacturer = manufacturer
        self.state = "Manufactured"
        self.distributor = None
        self.pharmacy = None
        self.consumer = None

class SupplyChain:
    def __init__(self):
        self.drugs = {}
        self.transactions = []

    def create_drug(self, drug_id, name, manufacturer):
        drug = Drug(drug_id, name, manufacturer)
        self.drugs[drug_id] = drug
        self.log_transaction(drug_id, "Manufactured", manufacturer)
        return drug

    def assign_distributor(self, drug_id, distributor):
        drug = self.drugs.get(drug_id)
        if drug and drug.state == "Manufactured":
            drug.distributor = distributor
            drug.state = "In Transit"
            self.log_transaction(drug_id, "In Transit", distributor)
        else:
            raise Exception("Drug is not in a state to be assigned to a distributor")

    def deliver_to_pharmacy(self, drug_id, pharmacy):
        drug = self.drugs.get(drug_id)
        if drug and drug.state == "In Transit":
            drug.pharmacy = pharmacy
            drug.state = "Delivered to Pharmacy"
            self.log_transaction(drug_id, "Delivered to Pharmacy", pharmacy)
        else:
            raise Exception("Drug is not in a state to be delivered to a pharmacy")

    def sell_to_consumer(self, drug_id, consumer):
        drug = self.drugs.get(drug_id)
        if drug and drug.state == "Delivered to Pharmacy":
            drug.consumer = consumer
            drug.state = "Sold to Consumer"
            self.log_transaction(drug_id, "Sold to Consumer", consumer)
        else:
            raise Exception("Drug is not in a state to be sold to a consumer")

    def log_transaction(self, drug_id, action, entity):
        timestamp = datetime.datetime.now()
        transaction_hash = self.generate_hash(drug_id, action, entity, timestamp)
        transaction = {
            "drug_id": drug_id,
            "action": action,
            "entity": entity,
            "timestamp": timestamp,
            "transaction_hash": transaction_hash
        }
        self.transactions.append(transaction)

    def generate_hash(self, drug_id, action, entity, timestamp):
        block_string = str(drug_id) + action + entity + str(timestamp)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def get_transaction_history(self, drug_id):
        return [t for t in self.transactions if t['drug_id'] == drug_id]

def main():
    supply_chain = SupplyChain()
    
    while True:
        print("\nPharma Supply Chain System")
        print("1. Manufacture Drug")
        print("2. Assign Distributor")
        print("3. Deliver to Pharmacy")
        print("4. Sell to Consumer")
        print("5. View Transaction History")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            drug_id = int(input("Enter Drug ID: "))
            name = input("Enter Drug Name: ")
            manufacturer = input("Enter Manufacturer Name: ")
            supply_chain.create_drug(drug_id, name, manufacturer)
            print(f"Drug {name} manufactured by {manufacturer}.")
        
        elif choice == '2':
            drug_id = int(input("Enter Drug ID: "))
            distributor = input("Enter Distributor Name: ")
            try:
                supply_chain.assign_distributor(drug_id, distributor)
                print(f"Drug {drug_id} assigned to distributor {distributor}.")
            except Exception as e:
                print(e)

        elif choice == '3':
            drug_id = int(input("Enter Drug ID: "))
            pharmacy = input("Enter Pharmacy Name: ")
            try:
                supply_chain.deliver_to_pharmacy(drug_id, pharmacy)
                print(f"Drug {drug_id} delivered to pharmacy {pharmacy}.")
            except Exception as e:
                print(e)

        elif choice == '4':
            drug_id = int(input("Enter Drug ID: "))
            consumer = input("Enter Consumer Name: ")
            try:
                supply_chain.sell_to_consumer(drug_id, consumer)
                print(f"Drug {drug_id} sold to consumer {consumer}.")
            except Exception as e:
                print(e)

        elif choice == '5':
            drug_id = int(input("Enter Drug ID: "))
            transaction_history = supply_chain.get_transaction_history(drug_id)
            if transaction_history:
                for transaction in transaction_history:
                    print(transaction)
            else:
                print("No transactions found for this drug.")

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
