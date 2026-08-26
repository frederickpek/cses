#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)


void solve() {
    int n, x, a;
    cin >> n >> x;
    vector<pair<int, int>> A(n);
    rep(i, n) {
        cin >> a;
        A[i] = make_pair(a, i + 1);
    }
    sort(A.begin(), A.end());

    int i = 0, j = n - 1;
    while (i < j) {
        int t = A[i].first + A[j].first;
        if (t == x) {
            cout << A[i].second << " " << A[j].second << endl;
            return;
        }
        if (t >= x) j--;
        else i++;
    }
    cout << "IMPOSSIBLE" << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    int t = 1;
    // cin >> t;
    while (t--) solve();
}
