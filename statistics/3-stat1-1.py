import numpy as np
import matplotlib.pyplot as plt

num_sim = 10000
n = 20
Mean = 5
Sigma = 1


means_arr = []
vars_arr = []
xmax_arr = []
for i in range(num_sim):
    # size = (сколько генераций, размер генерации)
    nd = np.random.normal(Mean, Sigma,  size=(1, n))
    # for j in nd:
    #     print(nd)
    # print(nd.mean())
    # # print(nd.sum() / 20)
    # print(nd.var(ddof=1))
    means_arr.append(nd.mean())
    # ddof - степени свободы (знаменать n - ddof)
    vars_arr.append((n-1) * nd.var(ddof=1) / Sigma**2)
    xmax_arr.append(nd.max())

# print(means_arr)
# print(vars_arr)
# print(xmax_arr)

# xMean ~ N(5, 1/20)
# т.к. 20 с.в.  x ~N(5, 1)
# (x1 + x2 + ... + x20) / 20 ~ N(5, 1/20)



fig, axs = plt.subplots(1, 3, figsize=(18, 5))

# Гистограмма для выборочного среднего с наложением теоретической плотности
# x_mean = np.linspace(mu - 4*sigma/np.sqrt(n), mu + 4*sigma/np.sqrt(n), 100)
axs[0].axvline((5 - Sigma / np.sqrt(20)), color='k', linestyle='dashed', linewidth=1)
axs[0].axvline((5 + Sigma / np.sqrt(20)), color='k', linestyle='dashed', linewidth=1)
axs[0].hist(means_arr, bins=30, density=True, alpha=0.6, color='skyblue', label='Эмпирическая')
# axs[0].plot(x_mean, norm.pdf(x_mean, loc=mu, scale=sigma/np.sqrt(n)), 'r-', lw=2, label='Теоретическая')
axs[0].set_title('Выборочное среднее')
axs[0].legend()

# # Гистограмма для статистики (n-1)S^2 с наложением плотности хи-квадрат
# x_chi = np.linspace(chi2.ppf(0.01, df=n-1), chi2.ppf(0.99, df=n-1), 100)
# axs[1].hist(chi_stat, bins=30, density=True, alpha=0.6, color='lightgreen', label='Эмпирическая')
# axs[1].plot(x_chi, chi2.pdf(x_chi, df=n-1), 'r-', lw=2, label='Теоретическая')
# axs[1].set_title('Статистика: (n-1)*S²/σ²')
# axs[1].legend()
#
# # Гистограмма для максимума выборки с наложением теоретической плотности
# x_max = np.linspace(mu - 3, mu + 3, 100)
# # Теоретическая плотность для Xmax:
# pdf_max = n * norm.pdf((x_max - mu) / sigma) * (norm.cdf((x_max - mu) / sigma))**(n - 1)
# axs[2].hist(sample_max, bins=30, density=True, alpha=0.6, color='salmon', label='Эмпирическая')
# axs[2].plot(x_max, pdf_max, 'r-', lw=2, label='Теоретическая')
# axs[2].set_title('Максимум выборки')
# axs[2].legend()

plt.tight_layout()
plt.show()