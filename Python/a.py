from Crypto.Util.number import long_to_bytes
from sympy.ntheory.modular import solve_congruence

# 假设中间解 m 已经通过前29个方程通过中国剩余定理解得到了
# 最后一个方程的参数
last_equation = (198538642, 143934548, 9310568, 156288812, 246408629)

# 验证中间解是否符合最后一个方程
if (a_last * intermediate_m**2 + b_last * intermediate_m + c_last) % mod_last == r_last:
    print("中间解 m 符合最后一个方程！")
    
    # 将中间解 m 转换为字节
    flag_bytes = long_to_bytes(intermediate_m)
    
    # 输出 flag
    print(f"Flag: {flag_bytes.decode()}")
else:
    print("中间解 m 不符合最后一个方程！需要调整或重新计算。")
