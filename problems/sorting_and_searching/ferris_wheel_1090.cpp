#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)


void solve() {
    int n, x;
    cin >> n >> x;
    vector<int> P(n);
    rep(i, n) cin >> P[i];
    sort(P.begin(), P.end());

    int i = 0, j = n - 1;
    int ans = n;
    while (i < j) {
        if (P[i] + P[j] <= x) {
            ans--; i++; j--;
            continue;
        }
        j--;
    }
    cout << ans << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    int t = 1;
    // cin >> t;
    while (t--) solve();
}
