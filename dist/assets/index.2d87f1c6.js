import{d as C,c as p,o as d,a as v,t as I,n as P,u as m,b as V,r as X,e as _,F as D,f as A,g as W,h as q,i as j,w as Q,j as U}from"./vendor.60301feb.js";const Z=function(){const e=document.createElement("link").relList;if(e&&e.supports&&e.supports("modulepreload"))return;for(const u of document.querySelectorAll('link[rel="modulepreload"]'))o(u);new MutationObserver(u=>{for(const s of u)if(s.type==="childList")for(const y of s.addedNodes)y.tagName==="LINK"&&y.rel==="modulepreload"&&o(y)}).observe(document,{childList:!0,subtree:!0});function a(u){const s={};return u.integrity&&(s.integrity=u.integrity),u.referrerpolicy&&(s.referrerPolicy=u.referrerpolicy),u.crossorigin==="use-credentials"?s.credentials="include":u.crossorigin==="anonymous"?s.credentials="omit":s.credentials="same-origin",s}function o(u){if(u.ep)return;u.ep=!0;const s=a(u);fetch(u.href,s)}};Z();var Y=(i,e)=>{const a=i.__vccOpts||i;for(const[o,u]of e)a[o]=u;return a};const G=C({props:{tab:null,curTab:null},setup(i){const e=i,a=p(()=>e.curTab.id==e.tab.id?e.tab.linkColor:"#fff"),o=p(()=>e.curTab.id==e.tab.id?"#fff":e.tab.linkColor);return(u,s)=>(d(),v("button",{class:"btn btn-outline-secondary",style:P({"box-shadow":"none",color:m(o),"border-color":i.tab.linkColor,"background-color":m(a)})},I(i.tab.name),5))}});var J=Y(G,[["__scopeId","data-v-1e911caa"]]);const R=C({props:{item:null,isSelected:{type:Boolean}},setup(i){const e=i,a=p(()=>e.item.id.split("-")[1]=="1"?"#F19D57":"");return(o,u)=>(d(),v("button",{type:"button",class:V(["btn btn-outline-secondary",e.isSelected?"active":""]),style:P({color:m(a)})},I(i.item.label),7))}});var ee=Y(R,[["__scopeId","data-v-4eaa0364"]]);const te=["id","transform"],le=["x","y","fill"],ne=["x","y"],ie=["cx","cy"],re=["x","y","fill"],oe=C({props:{link:null,linkStroke:null,tagName:null},emits:["deleteLink"],setup(i){const e=i,a=X(!1),o=p(()=>{let h=e.link.coordinates.split(" ")[1].split(",");return[Number(h[0].slice(1)),Number(h[1])]}),u=p(()=>Math.atan((e.link.start[1]-o.value[1])/(e.link.start[0]-o.value[0]))*180/Math.PI),s=p(()=>u.value*(e.link.start[1]-o.value[1])<0?1:-1),y=p(()=>Math.sqrt(Math.pow(e.link.start[1]-o.value[1],2)+Math.pow(e.link.start[0]-o.value[0],2))),x=p(()=>{if(e.link.linkType=="polyline")return;let h=s.value*40*(y.value/120)-10,t=u.value>0?14*(60/y.value):-14*(60/y.value)-10;return"rotate("+u.value+") translate("+h+","+t+")"}),f=p(()=>e.link.linkType=="polyline"?(e.link.start[0]+e.link.end[0])/2:e.link.start[0]),B=p(()=>e.link.linkType=="polyline"?e.link.highOffset-10:e.link.start[1]),$=p(()=>e.link.linkType=="polyline"?(e.link.start[0]+e.link.end[0])/2+18:e.link.start[0]+18),w=p(()=>e.link.linkType=="polyline"?e.link.highOffset+2:e.link.start[1]+13),z=p(()=>e.link.linkType=="polyline"?(e.link.start[0]+e.link.end[0])/2+36:e.link.start[0]+36),E=p(()=>e.link.linkType=="polyline"?e.link.highOffset-10:e.link.start[1]+2),H=p(()=>e.link.linkType=="polyline"?(e.link.start[0]+e.link.end[0])/2+38:e.link.start[0]+38),K=p(()=>e.link.linkType=="polyline"?e.link.highOffset-8:e.link.start[1]+2);return(h,t)=>(d(),v("g",{id:"link-tag-"+i.link.id,transform:m(x),style:{"transform-box":"fill-box","transform-origin":"center"},onMouseover:t[2]||(t[2]=n=>a.value=!0),onMouseout:t[3]||(t[3]=n=>a.value=!1)},[_("rect",{rx:"5",ry:"5",width:"36",height:"18",style:{position:"absolute","z-index":"5"},cursor:"pointer",x:m(f),y:m(B),fill:i.linkStroke},null,8,le),_("text",{"text-anchor":"middle",fill:"#fff","font-size":"10px",cursor:"pointer",style:{position:"absolute","z-index":"5"},x:m($),y:m(w)},I(i.tagName),9,ne),_("circle",{r:"8px",opacity:"0",cursor:"pointer",cx:m(z),cy:m(E),onClick:t[0]||(t[0]=n=>h.$emit("deleteLink"))},null,8,ie),_("text",{"text-anchor":"middle","font-size":"10px",cursor:"pointer",x:m(H),y:m(K),fill:a.value?i.linkStroke:"none",onClick:t[1]||(t[1]=n=>h.$emit("deleteLink"))}," x ",8,re)],40,te))}}),ue=["id"],se=["id"],ae=["fill"],ce=["marker-end","points","stroke"],de=C({props:{link:null,linkStroke:null},setup(i){return(e,a)=>(d(),v("g",{id:"link-line-"+i.link.id},[_("marker",{id:"arrow"+i.link.id,markerWidth:"8",markerHeight:"8",refX:"0",refY:"3",orient:"auto",markerUnits:"strokeWidth",viewBox:"0 0 20 20"},[_("path",{d:"M0,0 L0,6 L9,3 Z",fill:i.linkStroke},null,8,ae)],8,se),_("polyline",{fill:"none","stroke-width":"3","marker-end":"url(#arrow"+i.link.id+")",points:i.link.coordinates,stroke:i.linkStroke},null,8,ce)],8,ue))}}),ke=["id"],fe=["id"],pe=["fill"],ve=["marker-end","stroke","d"],me=C({props:{link:null,linkStroke:null},setup(i){return(e,a)=>(d(),v("g",{id:"link-line-"+i.link.id},[_("marker",{id:"arrow"+i.link.id,markerWidth:"8",markerHeight:"8",refX:"0",refY:"3",orient:"auto",markerUnits:"strokeWidth",viewBox:"0 0 20 20"},[_("path",{d:"M0,0 L0,6 L9,3 Z",fill:i.linkStroke},null,8,pe)],8,fe),_("path",{"stroke-width":"3",fill:"none","marker-end":"url(#arrow"+i.link.id+")",stroke:i.linkStroke,d:i.link.coordinates},null,8,ve)],8,ke))}});const ye={class:"link-draw"},_e={class:"line-draw"},ge={class:"tag-draw"},he=C({props:{links:null,tabs:null},emits:["deleteLink"],setup(i){return(e,a)=>(d(),v("div",ye,[(d(),v("svg",_e,[(d(!0),v(D,null,A(i.links.flat(),o=>(d(),W(q(o.linkType=="polyline"?de:me),{key:o.id,link:o,"link-stroke":i.tabs[o.relType].linkColor},null,8,["link","link-stroke"]))),128))])),(d(),v("svg",ge,[(d(!0),v(D,null,A(i.links.flat(),o=>(d(),W(oe,{key:o.id,link:o,"link-stroke":i.tabs[o.relType].linkColor,"tag-name":i.tabs[o.relType].name,onDeleteLink:u=>e.$emit("deleteLink",o)},null,8,["link","link-stroke","tag-name","onDeleteLink"]))),128))]))]))}});var be=Y(he,[["__scopeId","data-v-9ccd32ee"]]);const Fe={class:"words-view"},Ce=C({setup(i){const e="\u4E00\u4E2A\u5C0Fdemo",a=[{id:0,name:"\u5F53\u4E8B",linkColor:"#F1C757"},{id:1,name:"\u65BD\u4E8B",linkColor:"#6BB06C"},{id:2,name:"\u53D7\u4E8B",linkColor:"#57AAF1"},{id:3,name:"\u6D89\u4E8B",linkColor:"#8F6BB0"}],o=X(a[0]),u=[{id:0,items:[{id:"0-1",label:"\u5FEB\u9012\u5458"},{id:"0-2",label:"\u4F60"},{id:"0-3",label:"\u597D"},{id:"0-4",label:"\u5218\u5973\u58EB"},{id:"0-5",label:"\u8BF7"},{id:"0-6",label:"\u51FA\u6765"},{id:"0-7",label:"\u53D6"},{id:"0-8",label:"\u4E00\u4E0B"},{id:"0-9",label:"\u5FEB\u9012"}]},{id:1,items:[{id:"1-1",label:"\u5218\u5973\u58EB"},{id:"1-2",label:"\u6211"},{id:"1-3",label:"\u4E0D"},{id:"1-4",label:"\u5728\u5BB6"},{id:"1-5",label:"\u4F60"},{id:"1-6",label:"\u4E00"},{id:"1-7",label:"\u5C0F\u65F6"},{id:"1-8",label:"\u540E"},{id:"1-10",label:"\u518D"},{id:"1-11",label:"\u9001"},{id:"1-12",label:"\u5427"}]}];let s=X(""),y=[],x=[],f=X([[]]),B=0;const $=25;function w(t,n,l,r){let c=15-5*(r+1);t[0]>n[0]&&(c=-c);let b=(t[0]+20+c).toString()+","+t[1].toString(),T=(t[0]+20+c).toString()+","+l.toString(),g=(n[0]+20-c).toString()+","+l.toString(),F=(n[0]+20-c).toString()+","+(n[1]-10).toString();return b+" "+T+" "+g+" "+F}function z(t,n){if(s.value!=""){x=[n.offsetLeft,n.offsetTop];let l=n.offsetTop;y[1]==x[1]?E(y,x,l):(console.log("\u4E0D\u540C\u9AD8\u5EA6\u7684span\u8FDB\u884C\u8FDE\u63A5"),H(y,x))}else s.value=t.id,y=[n.offsetLeft,n.offsetTop]}function E(t,n,l,r=1,c=o.value.id,b=!1){let T=r;b&&(T+=1);for(let g=r;g<f.value.length;g++){let F=f.value[g];console.log(F);for(let S=0;S<F.length;S++){let k=F[S];if(t[1]!=k.start[1])continue;let L=t[0]<n[0]?t[0]:n[0],M=t[0]<n[0]?n[0]:t[0],N=k.start[0]<k.end[0]?k.start[0]:k.end[0],O=k.start[0]<k.end[0]?k.end[0]:k.start[0];if(M<=N||O<=L)console.log("\u60C5\u51B51\uFF1A\u65E0\u4EA4\u53C9\uFF0C\u5F85\u52A0\u5165\u5143\u7D20\u548C\u5F53\u524D\u5C42\u5143\u7D20\u7EE7\u7EED\u5BF9\u6BD4");else if(N<=L&&M<=O)console.log("\u60C5\u51B52\uFF1A\u5F53\u524D\u5143\u7D20\u5E94\u5305\u88F9\u52A0\u5165\u7684\u5143\u7D20"),F.splice(S,1),E(k.start,k.end,k.highOffset,g+1,k.relType);else if(L<=N&&O<=M){console.log("\u60C5\u51B53\uFF1A\u52A0\u5165\u7684\u5143\u7D20\u5E94\u5305\u88F9\u5F53\u524D\u5143\u7D20"),r+=1;break}else if(console.log("\u60C5\u51B54\uFF1A\u4EA4\u53C9\u4E14\u975E\u5305\u88F9\u5173\u7CFB\uFF0C\u957F\u5EA6\u8F83\u957F\u7684\u4E0A\u5347\u5230\u4E0A\u4E00\u5C42"),M-L>=O-N){r+=1;break}else F.splice(S,1),E(k.start,k.end,k.highOffset,g+1,k.relType)}if(r==g){l-=$*(r-T+1);let S={id:B++,coordinates:w(t,n,l,r),start:t,end:n,highOffset:l,relType:c,linkType:"polyline",level:r};F.push(S);break}}if(r==f.value.length){l-=$*(r-T+1);let g={id:B++,coordinates:w(t,n,l,r),start:t,end:n,highOffset:l,relType:c,linkType:"polyline",level:r};f.value.push([g])}s.value="",t=[],n=[]}function H(t,n){let l={id:B++,start:t,end:n,coordinates:"",highOffset:-1,relType:o.value.id,linkType:"curve",level:0};if(t[1]>n[1]){console.log("\u5411\u4E0A\u8FDE\u63A5"),l.start=[t[0]+20,t[1]],l.end=[n[0]+20,n[1]+42];let r=l.start[0].toString()+","+l.start[1].toString(),c=((t[0]+n[0])/2).toString()+","+((t[1]+n[1])/2).toString(),b=l.end[0].toString()+","+l.end[1].toString();l.coordinates="M"+r+" Q"+c+" "+b}else{console.log("\u5411\u4E0B\u8FDE\u63A5"),l.start=[t[0]+20,t[1]+40],l.end=[n[0]+20,n[1]-8];let r=l.start[0].toString()+","+l.start[1].toString(),c=((t[0]+n[0])/2).toString()+","+((t[1]+n[1])/2).toString(),b=l.end[0].toString()+","+l.end[1].toString();l.coordinates="M"+r+" Q"+c+" "+b}f.value[0].push(l),s.value="",t=[],n=[]}function K(){s.value="",y=[]}function h(t){if(t.level==0){f.value[0].splice(f.value[0].indexOf(t),1);return}let n=!1;for(let l=0;l<f.value.length;l++)for(let r=0;r<f.value[l].length;r++)if(n){let c=f.value[l][r],b=c.highOffset+$;f.value[l].splice(r,1),E(c.start,c.end,b,l-1,c.relType,!0)}else if(t===f.value[l][r]){f.value[l].splice(r,1),n=!0;break}}return(t,n)=>(d(),v(D,null,[_("h1",null,I(e)),(d(),v(D,null,A(a,l=>j(J,{key:l.id,tab:l,"cur-tab":o.value,class:V(o.value.id===l.id?"active":""),onClick:r=>o.value=l},null,8,["tab","cur-tab","class","onClick"])),64)),_("div",Fe,[(d(),v(D,null,A(u,l=>_("div",{class:V("utterance "+l.id),key:l.id},[(d(!0),v(D,null,A(l.items,r=>(d(),W(ee,{key:r.id,item:r,"is-selected":r.id===m(s),onClick:c=>z(r,c.target),onKeyup:Q(K,["esc"])},null,8,["item","is-selected","onClick","onKeyup"]))),128))],2)),64)),j(be,{links:m(f),onDeleteLink:h,tabs:a},null,8,["links"])])],64))}});var Se=Y(Ce,[["__scopeId","data-v-740c174a"]]);const xe={id:"main-panel"},Ee=C({setup(i){return(e,a)=>(d(),v("div",xe,[j(Se)]))}});U(Ee).mount("#app");
