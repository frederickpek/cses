#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define rep(i, n) for (int i = 0; i < n; i++)
const int N = 2e5 + 7;
ll A[N];


void solve() {
    int n, q, a, b;
    cin >> n >> q;
    rep(i, n) cin >> A[i + 1];
    rep(i, n) A[i + 1] += A[i];
    rep(i, q) {
        cin >> a >> b;
        cout << A[b] - A[a - 1] << endl;
    }
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    int t = 1;
    // cin >> t;
    while (t--) solve();
}
