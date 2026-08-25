#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)


const int INF = 1e9;

void solve() {
    int n, T;
    cin >> n >> T;
    vector<int> C(n);
    rep(i, n) cin >> C[i];

    vector<int> dp(T + 1, INF);
    dp[0] = 0;

    rep(i, T + 1) {
        for (int c : C) {
            if (i - c < 0) continue;
            dp[i] = min(dp[i], dp[i - c] + 1);
        }
    }

    cout << (dp[T] >= INF ? -1 : dp[T]) << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    solve();
}
