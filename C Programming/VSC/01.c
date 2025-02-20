#include <stdio.h>

// 计算阶乘
long long factorial(int n) {
    long long result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}

// 主函数
int main() {
    // 设置搜索范围
    int max_val = 10;  // 可以根据需要调整最大值

    for (int a = 1; a <= max_val; a++) {
        for (int b = 1; b <= max_val; b++) {
            // 计算阶乘和幂
            long long fact_a = factorial(a);
            long long fact_b = factorial(b);
            long long power_ab = 1;

            // 计算 a^b
            for (int i = 1; i <= b; i++) {
                power_ab *= a;
            }

            // 检查是否满足条件
            if (fact_a + fact_b == power_ab) {
                printf("找到解：a = %d, b = %d\n", a, b);
            }
        }
    }

    return 0;
}
