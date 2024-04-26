# def remove_duplicates(input_file, output_file):
#   unique_lines = []

#   with open(input_file, 'r') as input_csv:
#     for line in input_csv:
#       if not line.strip() in unique_lines:
#         unique_lines.append(line.strip())
#       else: print(line)

#   with open(output_file, 'w') as output_csv:
#     for line in unique_lines:
#       output_csv.write(line + '\n')

# remove_duplicates('data/stockton, ca.csv', 'new.csv')

# def remove_duplicates(input_file, output_file):
#   unique_lines = []
#   i = 0
  
#   header = [ 'Class', 'Incident', 'Crime', 'Date/Time', 'Location_Name', 'Address', 'Accuracy', 'Agency', 'keyword' ]
#   with open(output_file, 'w') as file:
#     writer = csv.writer(file)
#     writer.writerow(header)

#   with open(input_file, 'r') as input_csv:
#     for line in input_csv:
#       if not line.strip() in unique_lines:
#         unique_lines.append(line.strip())
#         with open(output_file, 'a') as output_csv:
#            output_csv.write(line.strip() + '\n')
#       else: 
#         i += 1 
#         print(i)

# remove_duplicates('results/stockton, ca.csv', 'new.csv')

def remove_duplicates(input_file, output_file):
    lists = set()

    with open(input_file, 'r') as lines:
        for line in lines:
            if len(line.split(',')) > 3:
              lists.add(line)
            else: print(line)

    lists = list(lists)

    sorted_data = sorted(lists, key=lambda x: x.split(',')[3], reverse=True)
    
    with open(output_file, 'w') as output_csv:
        for line in sorted_data:
            output_csv.write(line)

remove_duplicates('data/stockton, ca.csv', 'avoid.csv')    
