// Independently interpret the immutable binary stream, one entire source-role basis at a time.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using U8=std::uint8_t;using U32=std::uint32_t;using U64=std::uint64_t;
constexpr unsigned roles=111, stripes=15, symbols=16, bits=6, stride=stripes*symbols*bits;
constexpr unsigned bank=roles*stride, public_n=2*bank, fields=1034640, charts=5614, words=(stride+63)/64;
struct Add {U32 s,t;};
struct Line {std::array<U64,words> part;};
struct Edge {unsigned i,j,s,a,t,b;};
void need(bool b,const char* why){if(!b)throw std::runtime_error(why);}
std::vector<U8> file(const std::string& path){std::ifstream f(path,std::ios::binary|std::ios::ate);need(bool(f),"file");auto n=f.tellg();f.seekg(0);std::vector<U8> buf(n);f.read((char*)buf.data(),n);return buf;}
U32 u32(const U8*x){return U32(x[0])|(U32(x[1])<<8)|(U32(x[2])<<16)|(U32(x[3])<<24);}
unsigned u16(const U8*x){return x[0]+256*x[1];}
void xor_into(Line& a,const Line& b){for(unsigned k=0;k<words;++k)a.part[k]^=b.part[k];}
bool nonzero(const Line& a){U64 v=0;for(auto x:a.part)v|=x;return v!=0;}
void flip(Line& a,unsigned bit){a.part[bit/64]^=U64(1)<<(bit%64);}
unsigned gf(unsigned x,unsigned y){unsigned n=0;for(unsigned k=0;k<bits;k++)if((x>>k)&1)n^=y<<k;for(int j=10;j>=6;--j)if((n>>j)&1)n^=67<<(j-6);return n;}
std::array<std::array<unsigned,16>,64> powers(){std::array<std::array<unsigned,16>,64> v{};for(unsigned x=0;x<64;++x){v[x][0]=1;for(unsigned n=1;n<16;++n)v[x][n]=gf(v[x][n-1],x);}return v;}
struct Stream {std::vector<Add> adds;std::size_t first_split=0;unsigned n_split=0;std::size_t raw_cut=0,canonical_cut=0;};
Stream decode(const std::string& path,const std::vector<U8>& encoded){
    auto e=file(path);need(e.size()==9ULL*44129632,"stream size");std::vector<U8> arcs(charts*charts);
    for(unsigned i=0;i<encoded.size();i+=5)arcs[u16(&encoded[i])*charts+u16(&encoded[i+2])]=encoded[i+4];
    std::vector<int> site(fields,-1),ytag(fields,-1);for(unsigned i=0;i<bank;++i){site[i]=2+i/stride;site[i+bank]=0;ytag[i+bank]=i/stride;}
    std::array<unsigned,5> counts{};std::array<unsigned,9> moves{};unsigned fresh=public_n;Stream st;st.adds.reserve(41202832);
    for(std::size_t n=0,off=0;off<e.size();++n,off+=9){auto op=e[off];auto a=u32(&e[off+1]),b=u32(&e[off+5]);need(a<fields&&op>=1&&op<=4,"opcode");counts[op]++;
        if(op==1){need(a==fresh++&&b<charts&&site[a]==-1,"owned creation");site[a]=b;}
        if(op==2){need(b<fields&&a!=b&&site[a]>=0&&site[a]==site[b],"live cochart");
            if(ytag[a]>=0){need(ytag[b]==-1||ytag[a]==ytag[b],"cross-receiver Y mixing");ytag[b]=ytag[a];}
            if(a>=public_n && b>=bank&&b<public_n && site[b]>=1233&&site[b]<4383){if(st.n_split++==0)st.first_split=st.adds.size();}
            st.adds.push_back({a,b});}
        if(op==3){need(b<charts&&site[a]>=0,"move ownership");auto k=arcs[site[a]*charts+b];need(k>0,"nonincident move");moves[k]++;site[a]=b;}
        if(op==4){need(n>=43414672&&a>=public_n&&site[a]>=0&&b==0,"terminal retirement");site[a]=-1;}
        if(n+1==21501687)st.raw_cut=st.adds.size();if(n+1==22298007)st.canonical_cut=st.adds.size();
        if(n+1==21501687||n+1==22298007){for(unsigned k=0;k<bank;k++)need(site[k]==1&&site[bank+k]==0,"midpoint charts");}
    }
    for(unsigned k=0;k<bank;k++){need(site[k]==1&&site[bank+k]==5503+int(k/stride),"terminal physical sites");need(ytag[k]<0&&ytag[k+bank]==int(k/stride),"Y ownership");}
    for(unsigned k=public_n;k<fields;k++)need(site[k]==-1,"live owner at term");
    need(counts==std::array<unsigned,5>{0,714960,41202832,1496880,714960},"opcode census");
    need(moves[1]==799200&&moves[2]==650160&&moves[4]==34560&&moves[8]==12960,"geometry costs");need(st.n_split==17280,"split handoffs");return st;
}
struct Audit {
    const Stream& stream;const std::vector<U8>& canon;const std::vector<Edge>& edges;
    std::vector<U8> dirty;std::array<std::array<unsigned,16>,64> p=powers();
    std::vector<Line> state,wanted;std::vector<U8> live;
    Audit(const Stream& st,const std::vector<U8>& c,const std::vector<Edge>& e):stream(st),canon(c),edges(e),dirty(fields),state(fields),wanted(public_n),live(fields){}
    unsigned simulate(int source,bool omit,bool dirty_check=true){
        std::memset(state.data(),0,state.size()*sizeof(Line));std::memset(wanted.data(),0,wanted.size()*sizeof(Line));std::fill(live.begin(),live.end(),0);
        if(source<0){for(unsigned k=0;k<bank;k++){flip(state[k+bank],k%stride);flip(wanted[k+bank],k%stride);live[k+bank]=1;}}
        else{for(unsigned k=0;k<stride;k++){flip(state[source*stride+k],k);flip(wanted[source*stride+k],k);live[source*stride+k]=1;}
          for(unsigned i=0;i<roles;++i)if(canon[i*roles+source])for(unsigned k=0;k<stride;++k)flip(wanted[bank+i*stride+k],k);
          for(auto e:edges)if(e.j==unsigned(source))for(unsigned r=0;r<16;r++)for(unsigned q=0;q<16;q++){
            auto c=gf(p[e.b][r],p[e.a][q]);for(unsigned l=0;l<bits;l++){
              unsigned mask=gf(c,1U<<l);for(unsigned b=0;b<bits;b++)if((mask>>b)&1)flip(wanted[bank+e.i*stride+(e.t*16+r)*bits+b],(e.s*16+q)*bits+l);}}
        }
        for(std::size_t h=0;h<stream.adds.size();h++){
            if(h==stream.raw_cut){for(unsigned k=0;k<public_n;++k){Line expected{};if((source<0&&k>=bank)||(source>=0&&k<bank&&k/stride==unsigned(source)))flip(expected,k%stride);need(state[k].part==expected.part,"arbitrary X restoration and pure Y at Hub visit");}}
            if(h==stream.canonical_cut){std::array<unsigned,9> rows{0,1,2,4,8,9,14,30,59};unsigned owner=1021680;for(unsigned s=0;s<15;s++)for(unsigned p=0;p<16;p++)for(auto i:rows)for(unsigned b=0;b<6;b++){Line expected{};if(source>=0&&canon[i*roles+source])flip(expected,(s*16+p)*6+b);need(state[owner++].part==expected.part,"canonical owner exact basis");}need(owner==fields,"canonical owner range");}
            auto a=stream.adds[h];if(!live[a.s]||(omit&&h==stream.first_split))continue;
            live[a.t]=1;xor_into(state[a.t],state[a.s]);
        }
        unsigned mismatched=0;for(unsigned k=0;k<public_n;k++)mismatched+=(state[k].part!=wanted[k].part);
        if(dirty_check)for(unsigned k=public_n;k<fields;k++)if(!dirty[k]&&live[k]&&nonzero(state[k]))dirty[k]=1;
        return mismatched;
    }
};
int main(int argc,char** argv){try{
    need(argc==5,"usage replay STREAM DATADIR START END");std::string dir=argv[2];int start=std::stoi(argv[3]),end=std::stoi(argv[4]);
    auto canon=file(dir+"/canonical.dat"),arcs=file(dir+"/allowed.dat"),terms=file(dir+"/terms.dat");need(canon.size()==roles*roles&&terms.size()==6*42840,"oracle dimensions");
    std::vector<Edge> edges;for(unsigned i=0;i<terms.size();i+=6)edges.push_back({terms[i],terms[i+1],terms[i+2],terms[i+3],terms[i+4],terms[i+5]});
    Stream st=decode(argv[1],arcs);Audit a(st,canon,edges);unsigned each=0;
    for(int j=start;j<end;j++){auto diff=a.simulate(j,false);need(diff==0,"arbitrary original-column mismatch");each++;if((j+1)%10==0)std::cerr<<"checked role "<<j<<'\n';}
    auto dirty=std::count(a.dirty.begin()+public_n,a.dirty.end(),1);unsigned bad=0;
    if(start==-1&&end==111){need(dirty==714960,"dirty owners across complete basis");
       // Find the input support of the first genuine prepositioned X-to-Y handoff from actual data.
       for(int j=0;j<111&&!bad;j++)bad=a.simulate(j,true,false);need(bad>0,"omitted real D4 split did not change endpoint");}
    std::cout<<"{\"start\":"<<start<<",\"exclusive_end\":"<<end<<",\"exact_X_role_bases\":"<<(each-(start==-1))<<",\"exact_independent_Y_roles\":"<<(start==-1?111:0)<<",\"dirty_owners_seen\":"<<dirty<<",\"failed_output_rows_after_first_D4_read_omission\":"<<bad<<",\"raw_geometry_and_causality\":true,\"split_binary_handoffs\":"<<st.n_split<<"}\n";
    return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
