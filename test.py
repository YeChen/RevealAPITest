with open(r"c:\tmp\abc.txt", "w") as file:
    # Loop through numbers 1 to 10
    for i in range(1, 100000):
        # Write each line to the file
        file.write(f"abcd{i}\n")

print("File has been created and written to c:\\tmp\\abc.txt")