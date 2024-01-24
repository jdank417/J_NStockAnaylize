import openpyxl

file_path = 'C:\\Users\\Jason Dank\\PycharmProjects\\FMPStockAnaylize\\standardDiv.xlsx'
wb = openpyxl.load_workbook(file_path)
ws = wb.active

print('Total number of rows: ' + str(ws.max_row) + '. And total number of columns: ' + str(ws.max_column))

cell_value = ws['B2'].value
print('Type of value in B3:', type(cell_value))

if cell_value is not None:
    cell_value_str = str(cell_value)  # Convert to string
    print('The value in cell B3 is: ' + cell_value_str)
else:
    print('The value in cell B3 is None.')
