#include <bits/stdc++.h>
using namespace std;
#define rep(i, n) for (int i = 0; i < n; i++)
const int N = 1e2 + 7;
const int X = 1e3 + 7;
bool dp[N * X];
int C[N];

/*
    propagate backwards starting from larger numbers to avoid inf propagations
    additional note to not propagate self
*/

void solve() {
    int n;
    cin >> n;
    rep(i, n) cin >> C[i];

    int nx = accumulate(C, C + n, 0);

    rep(i, n) {
        for (int x = nx; x > 0; x--) {
            if (!dp[x]) continue;
            dp[x + C[i]] = 1;
        }
        dp[C[i]] = 1;
    }

    cout << accumulate(dp, dp + nx + 1, 0) << endl;
    rep(x, nx + 1) {
        if (!dp[x]) continue;
        cout << x << " ";
    }
    cout << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    int t = 1;
    // cin >> t;
    while (t--) solve();
}
