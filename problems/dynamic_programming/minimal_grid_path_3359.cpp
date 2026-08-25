#include <bits/stdc++.h>
using namespace std;
#define rep(i, n) for (int i = 0; i < n; i++)
const int N = 3e3 + 7;
bool dp[N][N];

/*
    sweep the diagonal with equal manhattan distance from start
    0 1 2 3 4
    1 2 3 4 5
    2 3 4 5 6
    3 4 5 6 7
    4 5 6 7 8
    look for smallest char next to dp=true in prev step
    extend sequence
*/

void solve() {
    int n;
    cin >> n;
    vector<string> G(n);
    for (auto &row : G) cin >> row;
    
    dp[0][0] = true;
    vector<char> ans = {G[0][0]};

    for (int d = 1; d < n * 2 - 1; d++) {
        char c = 'Z';
        for (int i = max(0, d - n + 1); i <= min(d, n - 1); i++) {
            int j = d - i;
            if (!(i > 0 && dp[i-1][j]) && !(j > 0 && dp[i][j-1])) continue;
            c = min(c, G[i][j]);
        }
        for (int i = max(0, d - n + 1); i <= min(d, n - 1); i++) {
            int j = d - i;
            if (!(i > 0 && dp[i-1][j]) && !(j > 0 && dp[i][j-1]) || G[i][j] != c) continue;
            dp[i][j] = true;
        }
        ans.emplace_back(c);
    }

    for (auto &x : ans) cout << x;
    cout << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    solve();
}
