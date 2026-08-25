#include <bits/stdc++.h>
using namespace std;
#define rep(i, n) for (int i = 0; i < n; i++)
const int MOD = 1e9 + 7;
const int N = 1e5 + 7;
const int M = 1e2 + 7;
int dp[N][M], X[N];

/*
    dp[i][j] be possible arrays for the first i elements for when X_i is j

    base cases:
    X[1] = 0: dp[i][j] = 1, for all j
    X[1] is revealed: dp[1][X[1]] = 1, all other dp[i][j] = 0
    for any X[i] revealed too: dp[i][X[i]] = 1, all others dp[i][j] = 0

    transition:
    (X_i)=j only possible if X_(i-1) in {j-1, j, j+1}
    dp[i][j] = dp[i-1][j-1] + dp[i-1][j] + dp[i-1][j+1]

    ans will then just be sum(dp[n][j] for j 1..m incl)
*/

void solve() {
	int n, m;
	cin >> n >> m;
    rep(i, n) cin >> X[i + 1];

    rep(i, n + 1) rep(j, m + 1) {
        if (i == 0 || j == 0) continue;

        // base cases
        if (i == 1) {
            if (X[i] == 0) dp[i][j] = 1;
            else dp[i][X[i]] = 1;
            continue;
        }
        if (X[i] != 0 && X[i] != j) {
            dp[i][j] = 0;
            continue;
        }

        // transition
        dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD;
        dp[i][j] = (dp[i][j] + dp[i-1][j-1]) % MOD;
        dp[i][j] = (dp[i][j] + dp[i-1][j+1]) % MOD;
    }

    int ans = 0;
    rep(j, m + 1) ans = (ans + dp[n][j]) % MOD;
    cout << ans << endl;
}


int main() {
	ios::sync_with_stdio(0);
	cin.tie(0); cout.tie(0);
    solve();
}
