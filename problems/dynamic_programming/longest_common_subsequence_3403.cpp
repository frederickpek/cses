#include <bits/stdc++.h>
using namespace std;
#define rep(i, n) for (int i = 0; i < n; i++)
const int N = 1e3 + 7;
int A[N], B[N], dp[N][N];

/*
    longest common subsequence + reconstruction

    dp[i][j] be length of LCS considering up to ith and jth elements of A and B
    base: dp[0][j], dp[i][0] = 0

    transition cases:
    A_i != B_j: dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    A_i == B_j: dp[i][j] = dp[i - 1][j - 1] + 1

*/

void solve() {
    int n, m;
    cin >> n >> m;
    rep(i, n) cin >> A[i + 1];
    rep(i, m) cin >> B[i + 1];

    rep(i, n + 1) rep(j, m + 1) {
        if (i == 0 || j == 0) continue;
        if (A[i] != B[j]) {
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            continue;
        }
        dp[i][j] = dp[i - 1][j - 1] + 1;
    }

    vector<int> ans;
    int i = n, j = m;
    while (i != 0 && j != 0) {
        if (A[i] == B[j]) {
            ans.emplace_back(A[i]);
            i--; j--;
        }
        else if (dp[i][j - 1] > dp[i - 1][j]) j--;
        else i--;
    }
    reverse(ans.begin(), ans.end());


    cout << dp[n][m] << endl;
    for (auto &x : ans) cout << x << " ";
    cout << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    int t = 1;
    // cin >> t;
    while (t--) solve();
}
