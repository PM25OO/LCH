#include <stdio.h>

int main() {
    // 数据定义
    const char *names[] = {"Alice", "Bob", "Charlie", "Diana"};
    int ages[] = {23, 45, 34, 29};
    double salaries[] = {50000.50, 62000.75, 48000.00, 53000.25};
    int n = sizeof(ages) / sizeof(ages[0]); // 数据项数

    // 输出表头
    printf("\n%-10s %-5s %-10s\n", "Name", "Age", "Salary");
    printf("--------------------------------\n");

    // 输出每行数据
    for (int i = 0; i < n; i++) {
        printf("%-10s %-5d %-10.2f\n", names[i], ages[i], salaries[i]);
    }

    return 0;
}
