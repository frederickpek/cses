#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define rep(i, n) for (int i = 0; i < n; i++)


void solve() {
    int n;
    cin >> n;
    vector<int> P(n);
    rep(i, n) cin >> P[i];
    sort(P.begin(), P.end());

    ll ans = 1;
    rep(i, n) {
        if (P[i] <= ans) {
            ans += P[i];
            continue;
        }
        break;
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
