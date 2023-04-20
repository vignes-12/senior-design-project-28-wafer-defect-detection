import csv 
with open('../../auto_run.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',', quotechar='"')
    for row in reader:
        x_start = int(row[0])
        y_start = int(row[1])
        x_steps = int(row[2])
        y_steps = int(row[3])
        total_images = int(row[4])
        fov = row[5]

x = x_steps
y = y_steps

print(x)
print(y)