(self.webpackChunklite=self.webpackChunklite||[]).push([[9068],{21356:(e,t,n)=>{"use strict";n.d(t,{x:()=>A,S:()=>D});var r=n(28655),o=n.n(r),l=n(71439),a=n(67294),i=n(12291),s=n(42631),u=n(89970),c=n(17920),p=n(60002),d=n(41236),f=n(86654),v=n(88817),h=n(70162),b=n(3369),m=n(965),g=n(58006),C=n(76532),y=n(1932),S=n(324),w=n(62181),P=n(95760),O=n(51512),E=n(65347),k=n(67297),I=n(55573),H=n(27952);function j(){var e=o()(["\n  fragment MultiVote_post on Post {\n    id\n    clapCount\n    creator {\n      id\n      ...SusiClickable_user\n    }\n    isPublished\n    ...SusiClickable_post\n    collection {\n      id\n      slug\n    }\n    isLimitedState\n    ...MultiVoteCount_post\n  }\n  ","\n  ","\n  ","\n"]);return j=function(){return e},e}var x=function(e){var t,n=e.post,r=e.buttonStyle,o=e.hasDialog,l=e.shouldShowResponsiveLabelText,j=void 0!==l&&l,x=e.shouldHideClapsText,A=void 0!==x&&x,D=e.shouldHideClapsCount,T=void 0!==D&&D,F=e.susiEntry,L=e.verticalClapsText,U=void 0!==L&&L,_=(0,m.CP)(),q=(0,C.H)().value,V=null!==(t=null==q?void 0:q.id)&&void 0!==t?t:"",M=(0,y.Tf)(n).viewerEdge,R=(0,k.v9)((function(e){return e.config.authDomain})),N=(0,k.b$)((function(e){return e.multiVote.clapsPerPost})),G=(0,i.I0)(),J=function(e){return G((0,E.at)(e))},Q=(0,P.Av)(),B=(0,O.pK)(),$=(0,I.l)(N,n,M),z=$.clapCount,K=$.viewerClapCount,W=$.viewerHasClappedSinceFetch,Y=a.useCallback((function(){if(K&&K>=h.S2)return"Viewer exceeded authorized claps limit.";J({postId:n.id,clapCount:z+1,viewerClapCount:K+1,viewerHasClappedSinceFetch:!0})}),[K,n.id,z]),X=a.useCallback((function(){if(!K)return"Viewer did not clap.";_(n,V,-K,M),J({postId:n.id,clapCount:z-K,viewerClapCount:0,viewerHasClappedSinceFetch:!0}),Q.event("post.clientUnvote",{postId:n.id,postIds:[n.id],unvoteCount:K,source:B})}),[K,n.id,z,V,M,B]),Z=a.useCallback((function(e){_(n,V,e,M),Q.event("post.clientUpvote",{postId:n.id,postIds:[n.id],voteCount:e,source:B})}),[n.id,V,M,B]),ee=(0,b.m)({onIncrementClaps:Y,onUndoClaps:X,onSubmitClapsAccumulated:Z}),te=ee.clappedAt,ne=ee.onFloatEnd,re=ee.removeBurst,oe=ee.clap,le=ee.undoClaps,ae=ee.isPopping,ie=ee.isShowingViewerClapCount,se=ee.burstOffsets,ue=ee.onPopEnd;a.useEffect((function(){return function(){var e;e={postId:n.id},G((0,E.HQ)(e))}}),[]);var ce,pe=n.collection,de=n.creator,fe=n.id,ve=n.isPublished,he=n.isLimitedState,be=(ce=!(!de||de.id!==V),he?"This feature is temporarily disabled":ve?ce?"You cannot applaud your own story":void 0:"You cannot applaud a draft"),me=(0,h.wH)(r,j),ge=me.isObvious,Ce=me.isSubtleForDesktop,ye=me.alwaysShowClapsLabel,Se=me.hasClapsLabel,we=me.buttonScale,Pe=!!(K&&K>0),Oe=!!(z&&z>0),Ee=pe&&pe.slug?(0,H.JLP)(R,pe.slug,fe):(0,H.kIi)(R,fe);return a.createElement(c.l,{isSubtleForDesktop:Ce,verticalClapsText:U},a.createElement(d.$,{isObvious:ge,buttonStyle:r,isSubtleForDesktop:Ce,disableReason:be},V||be?a.createElement(a.Fragment,null,ie&&a.createElement(S.N8,null,a.createElement(p.q,{count:K,clappedAt:te,placement:ge?"FAR":"NEAR",onFloatEnd:ne})),a.createElement(v.v,{isPopping:ae,onPopEnd:ue},a.createElement(u.d,{scale:we,canUndo:Pe,isCircle:ge,isFilled:Pe,isUndoSuppressed:se.length>0,disableReason:be,onClickAndHold:oe,onUndo:le,shouldHideClapsText:A})),se.map((function(e){return a.createElement(s.P,{key:e,isLarge:ge,offset:e,onBurstEnd:re})}))):a.createElement(w.R9,{operation:"register",post:n,user:n.creator,actionUrl:Ee,susiEntry:F},a.createElement(u.d,{isCircle:ge,scale:we}))),Oe&&!T&&(!ie||ye)&&a.createElement(f.W,{buttonStyle:r,isSubtleForDesktop:Ce},a.createElement(g._,{shouldShowNetwork:ge,post:n,clapCount:z,showFullNumber:W,hasLabel:Se,hasDialog:o,shouldShowResponsiveLabelText:Ce||j,shouldHideClapsText:A})))},A=(0,l.Ps)(j(),w.qU,w.Vm,g.U),D=function(e){var t;return a.createElement(O.cW,{source:{postId:null===(t=e.post)||void 0===t?void 0:t.id},extendSource:!0},a.createElement(x,e))}},66210:(e,t,n)=>{"use strict";n.d(t,{V:()=>h,k:()=>b});var r=n(28655),o=n.n(r),l=n(23493),a=n.n(l),i=n(71439),s=n(67294),u=n(95760),c=n(51512),p=n(27108),d=n(8403),f=n(21146);function v(){var e=o()(["\n  fragment PostScrollTracker_post on Post {\n    id\n    collection {\n      id\n    }\n    sequence {\n      sequenceId\n    }\n  }\n"]);return v=function(){return e},e}function h(e,t,n,r){var o=(0,u.Av)(),l=(0,c.pK)(),i=(0,d.he)(),v=(0,c.Qi)(),h=Date.now(),b=null,m=s.useCallback(a()((function(){if(e.current){var r=(0,f.L6)(e.current);if((0,f.pn)(r)){var a=Date.now(),s=(0,f.tM)(r),u=(0,f.UO)(),c=(0,f.t_)(),p=Math.round(s.top),d=Math.round(s.top+s.height),m=u.top,g=u.top+c.height,C=u.height,y={postIds:[t.id],collectionIds:[t.collection?t.collection.id:""],sequenceIds:[t.sequence?t.sequence.sequenceId:""],sources:n?["post_page"]:[v],tops:[p],bottoms:[d],areFullPosts:[!0],loggedAt:a,timeDiff:null!==b?Math.round(a-b):0,scrollTop:m,scrollBottom:g,scrollableHeight:C,viewStartedAt:h},S={referrer:i,referrerSource:l};n?o.event("post.streamScrolled",y,S):o.event("post.streamScrolled",y),b=a}}}),1e3),[t,n]);s.useEffect((function(){m();var e=null!=r&&r.current?(0,p.jC)(null==r?void 0:r.current):p.V6;return e.on("scroll_end",m),function(){e.off("scroll_end",m)}}),[m])}var b=(0,i.Ps)(v())},83024:(e,t,n)=>{"use strict";n.d(t,{Gj:()=>h,eu:()=>b,Sz:()=>m});var r=n(28655),o=n.n(r),l=n(59713),a=n.n(l),i=n(50361),s=n.n(i),u=n(71439),c=n(14391);function p(){var e=o()(["\n  fragment buildQuotePreviewParagraph_quote on Quote {\n    paragraphs {\n      id\n      text\n      type\n      markups {\n        end\n        start\n        type\n      }\n    }\n    startOffset\n    endOffset\n  }\n"]);return p=function(){return e},e}function d(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function f(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?d(Object(n),!0).forEach((function(t){a()(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):d(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function v(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}var h=function(e){var t=100;if(1!==e.paragraphs.length)return null;var n=s()(e.paragraphs[0]),r=n.text||"",o=0,l=e.startOffset||0,a=e.endOffset||r.length;if(r.length-a>t&&(r=r.substring(0,a+t)+"…"),l>t){var i=l-t;r="…"+r.substring(i),o=i-1}n.text=r,n.type=c.NJ.P,n.markups.unshift({end:a,start:l,type:c.Jh.HIGHLIGHT});var u,p=function(e,t){var n;if("undefined"==typeof Symbol||null==e[Symbol.iterator]){if(Array.isArray(e)||(n=function(e,t){if(e){if("string"==typeof e)return v(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?v(e,t):void 0}}(e))||t&&e&&"number"==typeof e.length){n&&(e=n);var r=0,o=function(){};return{s:o,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:o}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var l,a=!0,i=!1;return{s:function(){n=e[Symbol.iterator]()},n:function(){var e=n.next();return a=e.done,e},e:function(e){i=!0,l=e},f:function(){try{a||null==n.return||n.return()}finally{if(i)throw l}}}}(n.markups);try{for(p.s();!(u=p.n()).done;){var d=u.value;d.start-=o,d.end-=o}}catch(e){p.e(e)}finally{p.f()}return n},b=function(e){if(1!==e.paragraphs.length)return null;var t=e.paragraphs[0].text||"",n=e.startOffset||0,r=e.endOffset||t.length,o=t.slice(n,r);return o.length>=185&&(o=o.substring(0,185)+"..."),f(f({},e.paragraphs[0]),{},{text:o,type:c.NJ.P,markups:[{end:o.length,start:0,type:c.Jh.HIGHLIGHT,anchorType:null,href:null,linkMetadata:null,userId:null}],hasDropCap:null,dropCapImage:null})},m=(0,u.Ps)(p())}}]);
//# sourceMappingURL=https://stats.medium.build/lite/sourcemaps/9068.81cc309b.chunk.js.map