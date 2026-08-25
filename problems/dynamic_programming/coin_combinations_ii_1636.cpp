#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)

const int MOD = 1e9 + 7;

void solve() {
    int n, T;
    cin >> n >> T;
    vector<int> C(n);
    rep(i, n) cin >> C[i];

    vector<int> dp(T + 1);
    dp[0] = 1;

    for (auto &c : C) rep(i, T + 1) {
        if (i - c < 0) continue;
        dp[i] = (dp[i] + dp[i - c]) % MOD;
    }

    cout << dp[T] << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    solve();
}
