library(ggplot2)
N <- 100
n <- 50
M <- 20
k <- seq(0, M - 1, 1)

y <- choose(M, k) * choose(N - M, n - k) / choose(N, n)
y2 <- choose(n, k) * ((M / N)^k) * (((N - M) / N)^(n - k))

df1 <- data.frame(k = k, y = y, y2 = y2)

n <- 10
y <- choose(M, k) * choose(N - M, n - k) / choose(N, n)
y2 <- choose(n, k) * ((M / N)^k) * (((N - M) / N)^(n - k))

df2 <- data.frame(k = k, y = y, y2 = y2)

p1 <- ggplot(df1, aes(x = k)) +
  geom_line(aes(y = y, color = "#ff8800")) +
  geom_line(aes(y = y2, color = "blue"))

p2 <- ggplot(df2, aes(x = k)) +
  geom_line(aes(y = y, color = "#ff8800")) +
  geom_line(aes(y = y2, color = "blue"))

gridExtra::grid.arrange(p1, p2)
