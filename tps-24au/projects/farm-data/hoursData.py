import json

# Define the path to your JSON file
file_path = 'hours.json'

# Function to load data from JSON
def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Ensure the JSON is a list
        if not isinstance(data, list):
            data = [data]
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

# Function to interact with the user and handle their input
def handle_user_input(data):
    while True:
        print("\nWhat would you like to do?")
        print("1. Display all workers and their summaries")
        print("2. Search for a worker by name or ID")
        print("3. Search for a crop by name or ID")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            # Display unique workers
            summary = summarize_worker_hours_and_tasks(data)
            for worker_id, details in summary.items():
                print(f"\nWorker: {details['name']} (ID: {worker_id})")
                print(f"Total Time: {details['total_time']:.2f} hours")
                print("Tasks:")
                for task in details["tasks"]:
                    print(f"  - {task['task']}: {task['time']:.2f} hours")

        elif choice == "2":
            query = input("Enter part or all of the worker's name, or their ID: ").strip().lower()
            total_hours, task_list, matches = get_worker_hours(query, data)
            
            if matches:
                # Use a set to track printed workers and avoid duplicates
                printed_workers = set()

                print(f"\nMatches for '{query}':")
                for match in matches:
                    worker = match.get('worker', {})
                    worker_name = worker.get('name', 'Unknown Worker')
                    worker_id = worker.get('id') or match.get('worker_id')
                    
                    # Print worker details only if not already printed
                    if worker_id not in printed_workers:
                        print(f"  - Worker: {worker_name} (ID: {worker_id})")
                        printed_workers.add(worker_id)

                # Print total hours and task details
                print(f"\nTotal hours worked by workers matching '{query}': {total_hours:.2f} hours")
                print("Tasks:")
                for task in task_list:
                    print(f"  - {task}")
                else:
                    print(f"No workers found matching: {query}")

        elif choice == "3":
            query = input("Enter part or all of the crop's name, or its ID: ").strip().lower()
            total_hours, workers, matches = get_crop_data(query, data)

            if matches:
                print(f"\nMatches for crop '{query}':")
                for match in matches:
                    crop = match.get("harvest", {}).get("crop", {})
                    crop_name = crop.get("name", "Unknown Crop")
                    crop_id = crop.get("ID", match.get("crop_id"))
                    print(f"  - Crop: {crop_name} (ID: {crop_id})")

                print(f"\nTotal hours worked on '{query}': {total_hours:.2f} hours")
                print("Workers:")
                for worker in workers:
                    print(f"  - Worker: {worker['worker_name']} (ID: {worker['worker_id']})")
            else:
                print(f"No crops found matching: {query}")

        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Function to summarize worker tasks
# Function to summarize worker hours and tasks
def summarize_worker_hours_and_tasks(data):
    summary = {}

    for entry in data:
        worker = entry.get("worker", {})
        worker_id = worker.get("id") or entry.get("worker_id")
        worker_name = worker.get("name", "Unknown Worker")
        duration = entry.get("duration", 0)

        if worker_id not in summary:
            summary[worker_id] = {"name": worker_name, "total_time": 0, "tasks": []}

        # Extract task names
        task_names = get_task_names(entry)
        summary[worker_id]["total_time"] += duration
        for task_name in task_names:
            summary[worker_id]["tasks"].append({"task": task_name, "time": duration})

    return summary


# Function to get tasks for a specific worker
def get_worker_hours(query, data):
    totalHours = 0
    taskList = []
    matches = []
    queryLower = query.lower()
    seenWorkerIds = set()

    for entry in data:
        worker = entry.get("worker", {})
        workerId = worker.get("id") or entry.get("worker_id")
        workerName = worker.get("name", "Unknown Worker").lower()

        # Check if the query matches the worker's name or ID
        if queryLower in workerName or queryLower == str(workerId).lower():
            if workerId not in seenWorkerIds:
                matches.append(entry)
                seenWorkerIds.add(workerId)

            # Accumulate tasks and total hours
            taskNames = get_task_names(entry)
            duration = entry.get("duration", 0)
            totalHours += duration
            for task_name in taskNames:
                taskList.append(f"{task_name} - Duration: {duration} hours")

    return totalHours, taskList, matches


# Helper function to extract task names
def get_task_names(entry):
    taskNames = []

    process = entry.get("process", {})
    harvestInProcess = process.get("harvest", {})
    cropInProcess = harvestInProcess.get("crop", {})
    if cropInProcess:
        process_task_name = cropInProcess.get("name")
        if process_task_name:
            taskNames.append(f"Processing {process_task_name}")

    harvest = entry.get("harvest", {})
    crop_in_harvest = harvest.get("crop", {})
    if crop_in_harvest:
        harvest_task_name = crop_in_harvest.get("name")
        if harvest_task_name:
            taskNames.append(f"Harvesting {harvest_task_name}")

    if not taskNames:
        taskNames.append("Unknown Task")

    return taskNames

# Function to get who worked on what specified crop by name or ID
# and for how long
def get_crop_data(query, data):
    hoursWorked = 0
    workerList = []
    matches = []
    queryLower = query.lower()
    seenCropIds = set()

    for entry in data:
        crop = entry.get("harvest", {}).get("crop", {})
        cropId = crop.get("ID")
        cropName = crop.get("name", "Mystery Crop").lower()

        # Check if the query matches crop's name or ID
        if queryLower in cropName or queryLower == str(cropId).lower():
            if cropId not in seenCropIds:
                matches.append(entry)
                seenCropIds.add(cropId)

            # Add up workers and hours
            workerNames = get_worker_data(entry)
            workerList.extend(workerNames)
            hoursWorked += entry.get("duration", 0)

    return hoursWorked, workerList, matches

# Helper function to extract worker details from an entry
def get_worker_data(entry):
    workerNames = []

    worker = entry.get("worker", {})
    worker_name = worker.get("name", "Unknown Worker")
    worker_id = worker.get("ID", worker.get("worker_id"))

    if worker_name and worker_id:
        workerNames.append({"worker_name": worker_name, "worker_id": worker_id})

    return workerNames


# Main script
if __name__ == "__main__":
    data = load_data(file_path)
    
    if data:
        handle_user_input(data)
    else:
        print("No data to process.")
