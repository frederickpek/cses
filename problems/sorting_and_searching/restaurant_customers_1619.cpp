#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)


void solve() {
    int n, s, t;
    cin >> n;
    vector<pair<int, int>> vec;
    rep(i, n) {
        cin >> s >> t;
        vec.emplace_back(make_pair(s, 0));
        vec.emplace_back(make_pair(t, 1));
    }
    sort(vec.begin(), vec.end());

    int ans = 0;
    int cs = 0;
    for (auto& [t, is_end] : vec) {
        cs += is_end ? -1 : 1;
        ans = max(ans, cs);
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
