#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)

int main() {
	ios::sync_with_stdio(0);
	cin.tie(0); cout.tie(0);
	
}

void solve() {
	
}

int main() {
	int t;
	cin >> t;
	rep(tc, t) {
		printf("Case #%d: ", tc+1);
		solve();
	}
}

template<class T>
using min_heap = priority_queue<T, vector<T>, greater<T>>;

g++ -g -O2 -std=gnu++17 -static .cpp

#define ll long long
#define ld long double
#define ar array

// #define endl "\n";
#define pi M_PI
#define cot(x) tan(pi/2 - x)
#define acot(x) pi/2 - atan(x)
#define vi vector<int>
#define pb push_back
#define pii pair<int,int>
#define vii vector<pii>
#define all(v) v.begin(), v.end()
#define rep(i, n) for (int i = 0; i < n; i++)
#define forEach(a, v) for (auto& a : v)
#define ones(m) __builtin_popcount(m)
#define zeros(m) __builtin_popcount(~m)
#define sz(x) (int)(x).size()

bool visc[105][105];
memset(visc, 0, sizeof visc); // 2d array memset

//vectors
vector.assign(int size, int value);
vector.resize(int size)

PQs in C++ are max-heaps 
insert -values to convert to min heap or use greater<T> as cmp
priority_queue<pii, vii, greater<pii>> pq; // min-heap sorted by p.first

// custom comparators
auto comparator = [](State u, State v) {
	if (getDist(u) == getDist(v)) 
		return getAdd(u).compare(getAdd(v)) > 0;
	return getDist(u) > getDist(v);
};
priority_queue<State, vector<State>, decltype(comparator)> pq(comparator);
pq.top(); pq.pop();
pq.push(x);

// asc by first, desc by second pii
auto cmp = [](pii a, pii b) {
	if (a.first == b.first) 
		return a.second > b.second;
	return a.first < b.first;
};

// can pass in a method too
bool cmp(pair<int,int>& p1, pair<int,int>& p2) {
	return p1.second < p2.second;
}


// string methods
// s.find("seq") returns index of first occarance of the sequence
s.find("seq") == string::npos;		// string::npos -> -1 (true -> cannot find)
sort(&s[0] + pos, &s[0] + pos + 3);	// sort specific portion
s.push_back('c') 	// amortised constant
s.pop_back()		// amortised constant
getline(cin, s);
cin.ignore() // ignores newline after cin, prep for getline
s.erase(s.begin()+j); // erases char at index j
string s = t; // creats a new copy of string t, stored to s;

// count occurences
int occurrences(string &s, string &t) {
	int occ = 0;
	int pos = s.find(t, 0);
	while (pos != string::npos) {
		occ++;
		pos = s.find(t, pos + t.length());
	}
	return occ;
}

//ufds
int sz[n]; rep(i, n) sz[i]=1;	// optional
int p[n];
memset(p, -1, sizeof p);

int parent(int u) {
	if (p[u] == -1) return u;
	p[u] = parent(p[u]);
	return p[u];
}

void join(int u, int v) {
	u = parent(u);
	v = parent(v);
	if (u != v) p[u] = v; // ,sz[v]+=sz[u];
}

vector<int> v; // in sorted smallest lexicographic order
or int v[n];
do {
	// whatever
} while (next_permutation(v.begin(), v.end()));
while (next_permutation(v, v+n));

// diagonals
// const int d4i[4]={-1, -1, 1, 1}, d4j[4]={-1, 1, -1, 1};
const int d4i[4]={-1, 0, 1, 0}, d4j[4]={0, 1, 0, -1};
const int d8i[8]={-1, -1, 0, 1, 1, 1, 0, -1}, d8j[8]={0, 1, 1, 1, 0, -1, -1, -1};
 
void solve() {}
 
int main() {
	ios::sync_with_stdio(0);
	cin.tie(0); cout.tie(0);
 
	int t=1;
	read(t);
	FOR(t) {
		//write("Case #", i+1, ": ");
		solve();
	}
}

// when pruning of states is involved, 
// it is sometimes better to not sort. 
// very data set dependant.

void ternary_search() {
	int x, y;
	cin >> x >> y;
	auto f = [x, y](const double h) { return (x-2*h)*(y-2*h)*h; };

	double lo = some_lower_bound;
	double hi = some_upper_bound;
	for (int i = 0; i < 50; i++) {
		double delta = (hi-lo)/3.0;
		double m1 = lo + delta;
		double m2 = hi - delta;
		(f(m1)<f(m2)) ? lo = m1 : hi = m2;
		// < for max value, > for min value
	}
	printf("%.8f\n", f(lo));
	// f(lo) for the y val, lo for the x val
}
