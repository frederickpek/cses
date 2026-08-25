#include <bits/stdc++.h>
using namespace std;
#define rep(i, n) for (int i = 0; i < n; i++)
const int MOD = 1e9 + 7;
const int N = 1e3;
int dp[N][N];
char G[N][N];

void solve() {
	int n;
	cin >> n;
    rep(i, n) rep(j, n) cin >> G[i][j];
    if (G[0][0] == '.') dp[0][0] = 1;
    rep(i, n) rep(j, n) {
        if (G[i][j] == '*') continue;
        if (i > 0) dp[i][j] = (dp[i][j] + dp[i - 1][j]) % MOD;
        if (j > 0) dp[i][j] = (dp[i][j] + dp[i][j - 1]) % MOD;
    }

    cout << dp[n - 1][n - 1] << endl;
}

int main() {
	ios::sync_with_stdio(0);
	cin.tie(0); cout.tie(0);
    solve();
}
