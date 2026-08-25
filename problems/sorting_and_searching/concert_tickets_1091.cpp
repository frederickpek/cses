#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)


void solve() {
    int n, m, h, t;
    cin >> n >> m;
    multiset<int> ms;
    rep(i, n) {
        cin >> h;
        ms.insert(h);
    }
    rep(i, m) {
        cin >> t;
        auto it = ms.upper_bound(t);
        if (it == ms.begin()) {
            cout << -1 << endl;
            continue;
        }
        cout << *(--it) << endl;
        ms.erase(it);
    }
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    int t = 1;
    // cin >> t;
    while (t--) solve();
}
