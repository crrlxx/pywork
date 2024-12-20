import openpyxl
from openpyxl import load_workbook

'''
实现一个脚本，可以输入计算标的，最高参考值、最低参考值，预期值，现存值，单位值。
根据计算标的，输出操作计划及份数，操作计划按参考值区间的10%来输出，
操作逻辑为：
1.根据预期总值和当前总值，判断当前份数在哪个区间
2.然后根据区间，输出操作计划及份数，以斐波那契数列来决定投入或减少的份数
3.总共最多143份，根据当前总值计算出当前的份数和单元值
3.1.下一阶段如果是上升，接下来的三步操作及操作时的参考值
3.2.下一阶段如果是下降，接下来的三步操作及操作时的参考值
4.支持更新特定计算标的现存值和单位值
5.支持记录历史操作计划
6.支持查看所有计算标的
'''
file_path = "grid.xlsx"
def main():
    # 交互式菜单，获取需要的操作
    while True:
        print("欢迎使用, 输入操作(1.add/2.update/3.delete/4.query/5.exit):")
        choice = input("Please input:")
        if choice == "5":
            break
        elif choice == "1":
            # 如果是添加，输入计算标的，最高参考值、最低参考值，预期值，现存值，单位值 
            add_target()
        elif choice == "2":
            # 支持更新特定计算标的当前份数和单位价值
            print("请输入计算标的，当前份数，单位价值")
        elif choice == "3":
            # 删除特定计算标的
            print("请输入计算标的")
        elif choice == "4":
            # 输出操作水位及份数，计算出综合价值，
            print("请输入计算标的")
            read_excel(file_path, "Sheet1")
        else:
            print("输入有误，请重新输入")


def add_target():
    print("请输入计算标的，最高参考值、最低参考值，预期值，现存值，单位值 ")
    target, max_ref, min_ref, expect_val, current_val, unit_value = input().split(',')
    print("input return: ",target, max_ref, min_ref, expect_val, current_val, unit_value)
    print("Current database:\n")
    # 计算当前份数
    current_shares = current_val/unit_value
    # 根据当前值和目标值，计算当前单位值在区间内的位置
    current_percent = current_val/expect_val
    max_row = read_excel(file_path, "Sheet1")
    plan = get_operation_plan(float(max_ref), float(min_ref), int(current_percent), int(current_shares), float(unit_value))

    input_data = [[target, max_ref, min_ref, current_shares, unit_value]]
    input_data[0] = input_data[0] + plan
    write_excel(file_path, "Sheet1", max_row, input_data)

def read_excel(file_path, sheet_name):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]
    for row in sheet.rows:
        for cell in row:
            print(cell.value, "\t\|", end="")
        print()
    return sheet.max_row

def write_excel(file_path, sheet_name, max_row, value):
    index = len(value)
    workbook = load_workbook(file_path)
    sheet = workbook.active
    sheet.title = sheet_name
    for i in range(0, index):
        for j in range(0, len(value[i])):  
            sheet.cell(row=i+1+max_row, column=j+1, value=str(value[i][j]))
    workbook.save(file_path)
    print("Write successfully!")

def fibonacci(n):  
    """生成斐波那契数列"""  
    fib_sequence = [1, 1]  
    for i in range(2, n):  
        fib_sequence.append(fib_sequence[i - 1] + fib_sequence[i - 2])  
    print(fib_sequence)
    return fib_sequence  

def get_operation_plan(high_value, low_value, current_percent, current_shares, unit_value):  
    """根据当前单位值和参考值生成操作计划"""  
    # 按143份计算当前份数，然后根据区间位置输出操作计划
    drop_count = int((unit_value-low_value)/(high_value-low_value) /0.1)
    max_step = 143  
    current_step = int(max_step * current_percent)
    shares_per_step = int(current_shares / current_step)
    print("当前份数: %d, 每份shares数:%d", current_step, shares_per_step)
    fib_sequence = fibonacci(10)  # 生成前10个斐波那契数  

    increase_plans = []  
    decrease_plans = []  
    # 循环加fibonacci数，直到达到当前份数，然后根据当前份数和区间位置输出操作计划
    # 如果当前份数大于当前单元价值在的区间，则要减少，反之则增加  
    fib_count = 0
    for i in range(0, 10):
        fib_count += fib_sequence[i]
        if current_step <= fib_count:
            increase_plans.append((fib_sequence[i], round(float(unit_value * (1 + 0.1 * (i+1))), 2)))
            if i == 0:
                pass
            elif i == 1:
                decrease_plans.append((fib_sequence[i-1], round(float(unit_value * (1 - 0.1 * (i))), 2)))
            if i == 8:
                increase_plans.append((fib_sequence[i+1], round(float(unit_value * (1 + 0.1 * (i+2))), 2)))
            elif i == 9:
                pass
            else:
                increase_plans.append((fib_sequence[i+1], round(float(unit_value * (1 + 0.1 * (i+2))), 2)))
                increase_plans.append((fib_sequence[i+2], round(float(unit_value * (1 + 0.1 * (i+3))), 2)))
                decrease_plans.append((fib_sequence[i-1], round(float(unit_value * (1 - 0.1 * (i+1))), 2)))
                decrease_plans.append((fib_sequence[i-2], round(float(unit_value * (1 - 0.1 * (i+2))), 2)))
        else:
            pass


    # 输出操作计划和更新后的当前份数 
    print("increase_plans + decrease_plans:", increase_plans + decrease_plans)
    return increase_plans + decrease_plans


if __name__ == "__main__":
    main()
    # 示例调用  
    high_value = 100.0  # 假设最高参考值为100  
    low_value = 0.0    # 假设最低参考值为20  
    current_shares = 143 # 当前份数  
    unit_value = 40.0   # 当前单位值  

    # result = get_operation_plan(high_value, low_value, current_shares, unit_value)  
