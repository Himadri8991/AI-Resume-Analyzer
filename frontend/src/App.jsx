import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Tilt from 'react-parallax-tilt';
import { UploadCloud, FileText, ScanFace, TrendingUp, ShieldCheck, Stars, Zap, Users, Crosshair } from 'lucide-react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

function App() {
  const [files, setFiles] = useState([]);
  const [jd, setJd] = useState('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState(null);
  const [mode, setMode] = useState('standard');
  const fileInputRef = useRef(null);

  useEffect(() => {
    let interval;
    if (loading) {
      setProgress(0);
      interval = setInterval(() => {
        setProgress(prev => {
          if (prev < 85) return prev + Math.random() * 12;
          if (prev >= 85 && prev < 98) return prev + Math.random() * 1.5;
          return prev;
        });
      }, 400);
    } else {
      setProgress(100);
      const to = setTimeout(() => setProgress(0), 1000);
      return () => clearTimeout(to);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (files.length === 0) return alert("Please align target candidate documents.");
    
    setLoading(true);
    const formData = new FormData();
    files.forEach(f => formData.append('files', f));
    formData.append('job_description', jd);

    try {
      const res = await fetch('https://pi-resume-api.onrender.com', { method: 'POST', body: formData });
      const data = await res.json();
      setResults(data.results);
    } catch(err) {
      console.error(err);
      alert(`Neural sync error. AI Engine unreachable.\n\n[Debug info: ${err.message}]`);
    } finally {
      setLoading(false);
    }
  };

  const AnimatedText = ({ text }) => {
    return (
      <motion.div
        initial={{ y: 20, opacity: 0, filter: 'blur(10px)' }}
        animate={{ y: 0, opacity: 1, filter: 'blur(0px)' }}
        transition={{ duration: 1.2, type: 'spring' }}
        className="title-gradient-light dark:title-gradient-dark py-2"
      >
        {text}
      </motion.div>
    );
  };

  // 3D Candidate Card
  const TopCandidate = ({ cand, rank, massive = false }) => (
    <Tilt
      tiltMaxAngleX={8} tiltMaxAngleY={8} perspective={1000} transitionSpeed={1200}
      scale={1.02} glareEnable={true} glareMaxOpacity={0.15} glareColor="white" glarePosition="all"
      className={`${massive ? 'col-span-1 h-full' : 'h-full flex flex-col'}`}
    >
        <motion.div 
        layoutId={`candidate-${cand.name}-${rank}`}
        initial={{ opacity: 0, scale: 0.9, y: 30 }} 
        animate={{ opacity: 1, scale: 1, y: 0 }} 
        transition={{ delay: Math.min(0.05 * rank, 0.5), type: "spring", stiffness: 100, damping: 20 }}
        className={`glass-panel-light dark:glass-panel-dark h-full relative overflow-hidden group hover:shadow-[0_20px_40px_rgba(0,0,0,0.15)] dark:hover:neon-glow-dark hover:neon-glow-light transition-all duration-500 flex flex-col`}
        >
        <div className="absolute top-0 left-0 w-full h-[3px] bg-gradient-to-r from-brand-indigo via-brand-teal to-brand-pink opacity-80" />
        
        <div className={`flex flex-col flex-1 ${massive ? "p-8 md:p-10" : "p-6"}`}>
            <div className="absolute top-6 right-8">
            <div className={`font-display font-black tracking-tighter select-none ${massive ? 'text-8xl opacity-[0.05]' : 'text-6xl opacity-[0.08]'} group-hover:opacity-20 transition-opacity mix-blend-overlay text-white`}>
                #{rank}
            </div>
            </div>

            <h3 className={`font-display font-black mb-2 break-normal leading-tight w-full text-white group-hover:text-brand-teal transition-colors tracking-tight ${massive ? 'text-3xl lg:text-4xl pr-8' : 'text-2xl pr-8'}`}>
            {cand.name}
            </h3>
            
            <div className="text-sm font-semibold mb-8 flex items-center gap-2 text-brand-indigo dark:text-brand-teal uppercase tracking-widest drop-shadow-sm">
            <ScanFace size={18} strokeWidth={2.5}/> {cand.matched_roles?.[0]?.job_title || "Domain Expert"}
            </div>

            <div className={`grid grid-cols-3 gap-2 mb-8 bg-black/50 ${massive ? 'p-4 lg:p-6 rounded-3xl' : 'p-3 rounded-2xl'} border border-white/10 backdrop-blur-2xl shadow-inner w-full`}>
            <div className="flex flex-col items-center justify-center">
                <p className={`uppercase tracking-[0.1em] text-gray-400 mb-1 font-black font-display whitespace-nowrap ${massive ? 'text-[10px]' : 'text-[8px]'}`}>ATS Score</p>
                <div className="flex items-baseline justify-center gap-[2px]">
                    <p className={`font-display font-black bg-gradient-to-br from-brand-teal to-brand-blue bg-clip-text text-transparent drop-shadow-md tracking-tighter ${massive ? 'text-4xl lg:text-5xl' : 'text-3xl'}`}>
                    {Math.round(cand.ats_score)}
                    </p>
                    <span className={`font-black text-gray-500 ${massive ? 'text-lg' : 'text-sm'}`}>%</span>
                </div>
            </div>
            <div className="border-l border-white/10 flex flex-col items-center justify-center">
                <p className={`uppercase tracking-[0.1em] text-gray-400 mb-1 font-black font-display whitespace-nowrap ${massive ? 'text-[10px]' : 'text-[8px]'}`}>Experience</p>
                <p className={`font-display font-black text-white tracking-tighter drop-shadow-md ${massive ? 'text-3xl lg:text-4xl' : 'text-2xl'}`}>{Math.round(cand.experience)} <span className="text-xs font-bold text-gray-500 uppercase tracking-widest whitespace-nowrap">Yrs</span></p>
            </div>
            <div className="border-l border-white/10 flex flex-col items-center justify-center">
                <p className={`uppercase tracking-[0.1em] text-gray-400 mb-1 font-black font-display whitespace-nowrap ${massive ? 'text-[10px]' : 'text-[8px]'}`}>Matrix</p>
                <div className="flex items-baseline justify-center gap-[2px]">
                    <p className={`font-display font-black text-white tracking-tighter drop-shadow-md ${massive ? 'text-3xl lg:text-4xl' : 'text-2xl'}`}>{Math.round(cand.similarity_score)}</p>
                    <span className={`font-black text-gray-500 ${massive ? 'text-lg' : 'text-sm'}`}>%</span>
                </div>
            </div>
            </div>

            <div className="flex flex-col flex-1 space-y-6">
            <div className={`flex items-start gap-4 bg-gradient-to-br from-brand-pink/10 to-transparent border border-brand-pink/20 rounded-[1.5rem] shadow-[0_10px_30px_rgba(236,72,153,0.05)] w-full ${massive ? 'p-6' : 'p-4'}`}>
                <Stars size={massive ? 28 : 20} className="text-brand-pink shrink-0 drop-shadow-[0_0_10px_rgba(236,72,153,0.5)] mt-1"/>
                <div>
                <p className="text-[10px] font-black text-brand-pink uppercase tracking-widest mb-2 font-display drop-shadow-sm">Neural Synthesizer</p>
                <p className={`text-white font-medium leading-relaxed drop-shadow-sm ${massive ? 'text-lg' : 'text-sm'}`}>"{cand.suggestions[0]}"</p>
                </div>
            </div>
            
            <div className="pt-2 mt-auto">
                <p className="text-[10px] font-black tracking-[0.2em] uppercase text-gray-400 mb-4 font-display drop-shadow-sm">Competencies</p>
                <div className="flex flex-wrap gap-2">
                {cand.skills.slice(0, massive ? 8 : 5).map((skill, i) => (
                    <span key={i} className={`px-3 py-1.5 bg-white/10 shadow-[0_4px_15px_rgba(0,0,0,0.2)] rounded-xl text-[10px] font-bold border border-white/20 text-white uppercase tracking-wider backdrop-blur-md ${massive ? 'text-xs px-4 py-2' : ''}`}>
                    {skill}
                    </span>
                ))}
                {cand.skills.length > (massive ? 8 : 5) && <span className={`px-2 py-1.5 text-[10px] font-black text-gray-400 bg-black/40 rounded-xl border border-dashed border-gray-600 tracking-widest uppercase backdrop-blur-md shadow-inner ${massive ? 'text-xs px-4 py-2' : ''}`}>+{cand.skills.length - (massive ? 8 : 5)} MORE</span>}
                </div>
            </div>
            </div>
        </div>
        </motion.div>
    </Tilt>
  );

  const RadarComparisonRender = () => {
    if(!results || results.length < 2) return null;
    const c1 = results[0];
    const c2 = results[1];
    const data = [
      { subject: 'ATS Output', A: c1.ats_score, B: c2.ats_score },
      { subject: 'Domain Align', A: c1.similarity_score, B: c2.similarity_score },
      { subject: 'Seniority W.', A: Math.min(c1.experience * 10, 100), B: Math.min(c2.experience * 10, 100) },
      { subject: 'Skill Density', A: Math.min(c1.skills.length * 3, 100), B: Math.min(c2.skills.length * 3, 100) },
      { subject: 'Risk Optimization', A: Math.max(100 - (c1.missing_skills.length * 5), 0), B: Math.max(100 - (c2.missing_skills.length * 5), 0) },
    ];

    return (
      <div className="col-span-1 lg:col-span-2 flex flex-col items-center justify-center p-8 h-full min-h-[500px] relative">
           <motion.div animate={{ rotate: 360 }} transition={{ duration: 60, repeat: Infinity, ease: 'linear' }} className="absolute w-[400px] h-[400px] bg-brand-teal/10 dark:bg-brand-teal/20 blur-[100px] rounded-full z-0"/>
           <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:20px_20px] dark:opacity-20 opacity-50 z-0 mask-image:radial-gradient(black,transparent)"/>
           
           <motion.h2 
              initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ delay: 0.2, type: 'spring' }} 
              className="text-4xl md:text-5xl font-display font-black mb-8 text-center text-gray-900 dark:text-white drop-shadow-xl z-10 flex items-center justify-center gap-4"
            >
              <Crosshair size={42} className="text-brand-pink animate-pulse drop-shadow-[0_0_15px_rgba(236,72,153,0.6)]" strokeWidth={2.5}/> AI DUEL MATRIX
           </motion.h2>

           <ResponsiveContainer width="100%" height={450} className="z-10 drop-shadow-2xl filter">
             <RadarChart cx="50%" cy="50%" outerRadius={window.innerWidth < 1024 ? "55%" : "70%"} data={data}>
               <PolarGrid stroke="currentColor" className="text-gray-400 dark:text-gray-600 opacity-30" strokeDasharray="4 4"/>
               <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 13, fontWeight: 900, fontFamily: 'Space Grotesk', letterSpacing: '1px' }} />
               <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
               <Radar name={c1.name} dataKey="A" stroke="#14B8A6" strokeWidth={5} fill="url(#tealGradient)" fillOpacity={0.6} />
               <Radar name={c2.name} dataKey="B" stroke="#EC4899" strokeWidth={5} fill="url(#pinkGradient)" fillOpacity={0.6} />
               
               <defs>
                 <linearGradient id="tealGradient" x1="0" y1="0" x2="0" y2="1">
                   <stop offset="5%" stopColor="#14B8A6" stopOpacity={0.8}/>
                   <stop offset="95%" stopColor="#4F46E5" stopOpacity={0.2}/>
                 </linearGradient>
                 <linearGradient id="pinkGradient" x1="0" y1="0" x2="0" y2="1">
                   <stop offset="5%" stopColor="#EC4899" stopOpacity={0.8}/>
                   <stop offset="95%" stopColor="#4F46E5" stopOpacity={0.2}/>
                 </linearGradient>
               </defs>

               <Tooltip 
                  contentStyle={{ backgroundColor: 'rgba(255,255,255,0.85)', backdropFilter: 'blur(20px)', border: '1px solid rgba(0,0,0,0.05)', borderRadius: '24px', boxShadow: '0 30px 60px rgba(0,0,0,0.12)', color: '#0f172a' }}
                  itemStyle={{ fontSize: '16px', fontFamily: 'Space Grotesk', fontWeight: '900' }}
                  labelStyle={{ color: '#64748b', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '2px', fontWeight: 'bold' }}
               />
             </RadarChart>
           </ResponsiveContainer>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col relative w-full overflow-x-hidden text-gray-800 dark:text-gray-100 antialiased font-sans">
      
      {/* Intense Background Mesh Layer */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none -z-20">
            {/* Deep Dark Mode Auroras */}
            <div className="hidden dark:block">
                <motion.div animate={{ rotate: 360, scale: [1, 1.2, 1] }} transition={{ duration: 45, repeat: Infinity, ease: "linear" }} className="aurora-orb w-[800px] h-[800px] bg-brand-indigo/15 -top-[20%] left-[10%]" />
                <motion.div animate={{ rotate: -360, scale: [1, 1.3, 1] }} transition={{ duration: 60, repeat: Infinity, ease: "linear" }} className="aurora-orb w-[900px] h-[900px] bg-brand-pink/10 -bottom-[10%] right-[0%]" />
                <motion.div animate={{ y: [0, -100, 0] }} transition={{ duration: 30, repeat: Infinity, ease: "easeInOut" }} className="aurora-orb w-[600px] h-[600px] bg-brand-teal/15 top-[30%] left-[40%]" />
            </div>
      </div>
      
      {/* Centered Awwwards Landing */}
      <motion.div initial={{ y: -50, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }} className="w-full relative pt-28 pb-16 px-4 flex flex-col items-center justify-center z-10 text-center">
        
        {/* Hover-Reactive Logo */}
        <Tilt tiltMaxAngleX={15} tiltMaxAngleY={15} perspective={800} scale={1.05} transitionSpeed={1000} className="relative z-20 cursor-pointer">
          <motion.div initial={{ scale: 0.5, filter: 'blur(20px)' }} animate={{ scale: 1, filter: 'blur(0px)' }} transition={{ delay: 0.3, duration: 1.2, type: 'spring', bounce: 0.5 }} className="relative mb-8 group">
            <div className="absolute inset-0 bg-gradient-to-tr from-brand-indigo via-brand-teal to-brand-pink blur-[60px] opacity-40 dark:opacity-60 rounded-full group-hover:blur-[90px] group-hover:opacity-80 transition-all duration-700 mix-blend-screen" />
            <img src="/logo.png" alt="PI Enterprise Logo" className="relative w-48 h-48 md:w-64 md:h-64 object-contain drop-shadow-[0_20px_50px_rgba(0,0,0,0.4)] dark:drop-shadow-[0_0_40px_rgba(255,255,255,0.1)]" />
          </motion.div>
        </Tilt>

        <h1 className="text-6xl md:text-[6rem] lg:text-[7.5rem] font-display font-black tracking-tighter leading-none mb-6">
          <AnimatedText text="Enterprise AI" />
        </h1>
        
        <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1 }} className="text-xl md:text-3xl text-gray-700 dark:text-gray-300 font-bold tracking-tight flex items-center justify-center gap-4 font-display">
          Pentaverse OS <Stars size={28} className="text-brand-pink drop-shadow-lg animate-pulse"/> Resume Evaluator
        </motion.p>
      </motion.div>

      {/* Main Form Dashboard */}
      <div className="w-full max-w-[1500px] mx-auto p-4 md:p-8 z-10 relative">
        <form onSubmit={handleUpload} className="w-full max-w-6xl mx-auto glass-panel-light dark:glass-panel-dark p-8 md:p-14 mb-20 relative overflow-hidden group/form shadow-[0_40px_100px_rgba(0,0,0,0.1)] dark:shadow-[0_40px_100px_rgba(0,0,0,0.8)]">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 md:gap-16 relative z-10">
            
            {/* Interactive Magnetic Dropzone */}
            <div className="flex flex-col">
              <label className="text-base font-display uppercase tracking-widest text-brand-indigo dark:text-brand-teal mb-5 font-black flex items-center gap-3 drop-shadow-sm">
                <FileText size={22} strokeWidth={3}/> Source Documents
              </label>
              <motion.div 
                  whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.99 }}
                  onClick={() => fileInputRef.current.click()}
                  className="relative flex-1 cursor-pointer border-[3px] border-dashed border-gray-300/80 dark:border-white/10 hover:border-brand-indigo dark:hover:border-brand-teal rounded-[2.5rem] bg-white/30 dark:bg-[#050810]/50 p-10 flex flex-col items-center justify-center transition-all duration-300 overflow-hidden shadow-inner min-h-[350px]"
              >
                <input ref={fileInputRef} type="file" multiple onChange={(e) => setFiles(Array.from(e.target.files))} className="hidden" />
                <div className="w-28 h-28 rounded-full bg-white dark:bg-black/60 shadow-[0_20px_50px_rgba(0,0,0,0.08)] dark:shadow-[0_20px_50px_rgba(0,0,0,0.5)] flex items-center justify-center mb-8 hover:scale-110 transition-transform duration-500 relative z-10">
                    <UploadCloud size={48} className="text-brand-indigo dark:text-brand-teal transition-colors drop-shadow-md" />
                </div>
                {files.length === 0 ? (
                    <div className="text-center">
                        <p className="text-gray-900 dark:text-white font-display font-black text-3xl tracking-tight mb-3">Drop Massive Batches</p>
                        <p className="text-gray-500 dark:text-gray-400 font-bold text-sm tracking-wide">PDF, DOCX formats mapped to SBERT.</p>
                    </div>
                ) : (
                    <div className="text-center scale-110 animate-pulse-slow">
                        <p className="text-brand-indigo dark:text-brand-teal font-display font-black text-6xl tracking-tighter drop-shadow-lg">{files.length}</p>
                        <p className="text-gray-700 dark:text-gray-300 font-black uppercase tracking-widest mt-3 text-sm">Resumes Buffered</p>
                    </div>
                )}
              </motion.div>
            </div>

            <div className="flex flex-col h-full">
              <label className="text-base font-display uppercase tracking-widest text-brand-pink mb-5 font-black flex items-center gap-3 drop-shadow-sm">
                <ScanFace size={22} strokeWidth={3}/> JD Parameters (Optional)
              </label>
              <textarea 
                placeholder="Paste the target Job Description...&#10;&#10;If omitted, PI Neural Framework parses inputs and auto-binds to 130+ O*NET targets seamlessly based on the highest embedded SBERT vectors." 
                value={jd} onChange={(e) => setJd(e.target.value)}
                className="flex-1 w-full bg-white/50 dark:bg-[#050810]/40 border-[3px] border-transparent hover:border-brand-pink/40 rounded-[2.5rem] p-10 text-xl text-gray-900 dark:text-white font-semibold focus:outline-none focus:border-brand-pink transition-all resize-none shadow-inner min-h-[350px] leading-relaxed placeholder:text-gray-400 dark:placeholder:text-gray-600"
              />
            </div>
          </div>

          <div className="mt-16 flex justify-center w-full relative z-10">
            <button 
              type="submit" disabled={loading}
              className="group/btn relative w-full md:w-auto px-24 py-7 rounded-[2.5rem] font-display font-black text-2xl uppercase tracking-[0.2em] overflow-hidden shadow-[0_20px_60px_rgba(20,184,166,0.25)] hover:shadow-[0_20px_80px_rgba(20,184,166,0.5)] dark:shadow-[0_20px_60px_rgba(236,72,153,0.25)] dark:hover:shadow-[0_20px_80px_rgba(236,72,153,0.5)] disabled:opacity-50 transition-all transform hover:-translate-y-1"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-brand-indigo via-brand-teal to-brand-pink opacity-90 group-hover/btn:scale-110 transition-transform duration-1000 ease-out"/>
              {loading ? (
                <div className="relative w-full h-full flex flex-col items-center justify-center gap-2 text-white drop-shadow-lg z-10">
                    <div className="flex items-center gap-4">
                        <div className="w-6 h-6 border-[3px] border-white/20 border-t-white rounded-full animate-spin" /> 
                        <span>ALGORITHMS CALCULATING ( {Math.floor(progress)}% )</span>
                    </div>
                    <div className="w-[80%] h-1.5 bg-black/20 rounded-full overflow-hidden mt-2 relative">
                        <motion.div initial={{ width: 0 }} animate={{ width: `${progress}%` }} className="h-full bg-white transition-all duration-300 ease-out" />
                    </div>
                </div>
              ) : (
                <span className="relative z-10 flex items-center justify-center gap-5 text-white drop-shadow-lg"><Zap size={32} fill="currentColor"/> INITIATE SEQUENCE</span>
              )}
            </button>
          </div>
        </form>

        {/* --- LIVE DEMO PREVIEW (EMPTY STATE) --- */}
        {!results && !loading && (
            <motion.div initial={{ opacity: 0, y: 100 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5, duration: 1.5, type: 'spring' }} className="w-full relative z-0 pb-40 scale-95 opacity-50 md:scale-100 pointer-events-none select-none">
              
              <div className="flex justify-center mb-10 relative z-30">
                <div className="inline-flex p-2 bg-white/10 dark:bg-black/40 rounded-full border border-gray-200/50 dark:border-white/5 backdrop-blur-md">
                    <button className="px-10 py-4 rounded-full text-sm font-black uppercase tracking-widest transition-all duration-300 font-display text-gray-400">Standard Array Grid</button>
                    <button className="px-10 py-4 flex items-center justify-center gap-3 rounded-full text-sm font-black uppercase tracking-widest transition-all duration-300 font-display bg-gradient-to-r from-brand-pink/50 to-brand-indigo/50 text-white shadow-[0_15px_40px_rgba(236,72,153,0.2)] blur-[1px]">
                        <Crosshair size={22} className="opacity-50" /> Candidate Duel
                    </button>
                </div>
              </div>

              <div className="flex flex-col items-center justify-center mb-16 pb-8 border-b-[3px] border-white/5">
                <h2 className="text-4xl font-display font-black flex items-center gap-6 text-gray-500/50 tracking-tighter">
                    <TrendingUp className="text-brand-pink/50 opacity-50" size={42} strokeWidth={3}/> Live Layout Preview (Awaiting Data)
                </h2>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 md:gap-12 opacity-40 blur-sm pointer-events-none">
                <div className="glass-panel-dark h-[600px] border-2 border-dashed border-white/10 flex items-center justify-center col-span-1 rounded-[2.5rem]">
                    <span className="text-xl font-bold uppercase tracking-widest text-white/30 rotate-90">Alpha Node</span>
                </div>
                <div className="col-span-2 flex items-center justify-center h-[600px] relative">
                    <div className="absolute w-[300px] h-[300px] rounded-full border border-brand-teal/20 animate-ping" />
                    <div className="absolute w-[400px] h-[400px] rounded-full border border-brand-indigo/10 animate-pulse" />
                    <Crosshair size={100} className="text-white/10" strokeWidth={1} />
                </div>
                <div className="glass-panel-dark h-[600px] border-2 border-dashed border-white/10 flex items-center justify-center col-span-1 rounded-[2.5rem]">
                    <span className="text-xl font-bold uppercase tracking-widest text-white/30 -rotate-90">Beta Node</span>
                </div>
              </div>
            </motion.div>
        )}

        <AnimatePresence>
          {results && !loading && (
            <motion.div initial={{ opacity: 0, scale: 0.95, filter: 'blur(20px)' }} animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }} transition={{ duration: 1, type: 'spring', bounce: 0.2 }} className="w-full relative z-20 pb-40">
              
              {/* Massive Toggle UI Array */}
              <div className="flex justify-center mb-16 relative z-30">
                <div className="inline-flex p-2 bg-white/70 dark:bg-[#0f172a]/60 rounded-full border border-gray-200 shadow-2xl dark:border-white/10 backdrop-blur-2xl">
                    <button onClick={() => setMode('standard')} className={`px-10 py-5 rounded-full text-base font-black uppercase tracking-widest transition-all duration-300 font-display ${mode === 'standard' ? 'bg-gradient-to-r from-brand-indigo to-brand-teal text-white shadow-[0_15px_40px_rgba(20,184,166,0.4)]' : 'text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white hover:bg-white/50 dark:hover:bg-white/5'}`}>
                        Standard Array Grid
                    </button>
                    <button onClick={() => setMode('compare')} className={`px-10 py-5 flex items-center justify-center gap-3 rounded-full text-base font-black uppercase tracking-widest transition-all duration-300 font-display ${mode === 'compare' ? 'bg-gradient-to-r from-brand-pink to-brand-indigo text-white shadow-[0_15px_40px_rgba(236,72,153,0.4)]' : 'text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white hover:bg-white/50 dark:hover:bg-white/5'}`}>
                        <Crosshair size={22} className={mode === 'compare' ? 'animate-spin-slow' : ''} /> Candidate Duel
                    </button>
                </div>
              </div>

              <div className="flex flex-col items-center justify-between xl:flex-row mb-12 pb-8 border-b-[3px] border-gray-200 dark:border-white/10">
                <h2 className="text-5xl md:text-6xl font-display font-black flex items-center gap-6 text-gray-900 dark:text-white tracking-tighter drop-shadow-md">
                    <TrendingUp className="text-brand-pink" size={56} strokeWidth={3}/> {mode === 'standard' ? 'Output Array' : 'Duel Matrix Results'}
                </h2>
                <div className="mt-8 xl:mt-0 font-display text-base font-black uppercase tracking-[0.2em] bg-white dark:bg-black/80 text-brand-indigo dark:text-brand-teal px-8 py-4 rounded-full border-2 border-brand-indigo/20 dark:border-brand-teal/20 shadow-lg">Network Scale: {results.length} Nodes</div>
              </div>

              {/* Total Layout Shift Logic */}
              <motion.div layout className={`w-full max-w-[1500px] mx-auto mt-12 transition-all duration-700 ease-in-out ${mode === 'compare' ? 'flex flex-col lg:flex-row items-stretch justify-between gap-8' : 'grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8 items-stretch'}`}>
                  
                  <AnimatePresence mode='wait'>
                    {mode === 'compare' ? (
                        <motion.div key="compare-mode" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="w-full flex flex-col col-span-full">
                            <div className="flex flex-col lg:flex-row items-stretch justify-between gap-8 w-full">
                                <motion.div layout initial={{ opacity: 0, x: -100 }} animate={{ opacity: 1, x: 0 }} transition={{ type: 'spring', bounce: 0 }} className="w-full lg:w-[420px] shrink-0 z-20">
                                  <TopCandidate key={`compare-${results[0].name}-1`} cand={results[0]} rank={1} massive={true} />
                                </motion.div>
                                
                                <motion.div layout initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.2, type: 'spring' }} className="w-full lg:flex-1 min-w-[300px] flex items-center justify-center relative z-10">
                                  <div className="w-full relative py-10 flex flex-col items-center">
                                    <RadarComparisonRender />
                                  </div>
                                </motion.div>
                                
                                <motion.div layout initial={{ opacity: 0, x: 100 }} animate={{ opacity: 1, x: 0 }} transition={{ type: 'spring', bounce: 0 }} className="w-full lg:w-[420px] shrink-0 z-20">
                                  <TopCandidate key={`compare-${results[1].name}-2`} cand={results[1]} rank={2} massive={true} />
                                </motion.div>
                            </div>

                            {/* Runner Ups */}
                            {results.length > 2 && (
                                <div className="w-full mt-24">
                                    <h3 className="text-3xl font-display font-black text-center mb-10 text-gray-500 dark:text-gray-400 uppercase tracking-widest">Runners Up</h3>
                                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8 items-stretch">
                                        {results.slice(2).map((c, i) => <TopCandidate key={`cand-rest-${c.name}-${i+3}`} cand={c} rank={i+3} massive={false} />)}
                                    </div>
                                </div>
                            )}
                        </motion.div>
                    ) : (
                        <motion.div key="standard-mode" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="w-full col-span-full grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8 items-stretch">
                            {results.map((c, i) => (
                                <TopCandidate key={`cand-std-${c.name}-${i+1}`} cand={c} rank={i+1} massive={false} />
                            ))}
                        </motion.div>
                    )}
                  </AnimatePresence>

              </motion.div>

            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </div>
  );
}

export default App;
