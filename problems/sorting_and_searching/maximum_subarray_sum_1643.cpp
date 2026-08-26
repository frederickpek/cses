#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define rep(i, n) for (int i = 0; i < n; i++)
const int N = 2e5 + 7;
int A[N];

void solve() {
    int n;
    cin >> n;
    rep(i, n) cin >> A[i];

    ll cs = 0;
    ll ans = -1e9;
    rep(i, n) {
        cs += A[i];
        ans = max(ans, cs);
        cs = max(cs, (ll) 0);
    }

    cout << ans << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    solve();
}
