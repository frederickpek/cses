#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)

const int INF = 1e9;

void solve() {
    int n;
    cin >> n;
    vector<int> dp(n + 1, INF);
    dp[0] = 0;

    /*
        dp[i] = min(dp[i - k]) + 1, for each k in numeric rep of i, less 0
    */

    rep(i, n + 1) {
        for (auto &c : to_string(i)) {
            int k = c - '0';
            if (k == 0 || i - k < 0) continue;
            dp[i] = min(dp[i], dp[i - k] + 1);
        }
    }

    cout << dp[n] << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    solve();
}
