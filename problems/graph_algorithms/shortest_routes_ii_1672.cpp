#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)

const long long INF = 1e18;

void solve() {
	int n, m, q;
	cin >> n >> m >> q;

	vector<vector<long long>> D(n, vector<long long>(n, INF));
	rep(i, n) D[i][i] = 0;
	rep(i, m) {
		int u, v;
		long long w;
		cin >> u >> v >> w;
		u--; v--;
		D[u][v] = min(w, D[u][v]);
		D[v][u] = min(w, D[v][u]);
	}

	// floyd warshall
	rep(k, n) rep(u, n) rep(v, n) {
		D[u][v] = min(D[u][v], D[u][k] + D[k][v]);
	}

	rep(i, q) {
		int u, v;
		cin >> u >> v;
		long long ans = D[u - 1][v - 1];
		cout << (ans >= INF ? -1 : ans) << endl;
	}
}

int main() {
	ios::sync_with_stdio(0);
	cin.tie(0); cout.tie(0);
    solve();
}
