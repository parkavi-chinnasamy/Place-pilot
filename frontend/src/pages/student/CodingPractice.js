import React, { useState } from 'react';
import { Card, PageHeader, Btn, Badge, DemoBanner } from '../../components/common/Card';
import { FiCode, FiPlay, FiCheck } from 'react-icons/fi';

const PROBLEMS = [
  { id:1, title:'Two Sum', difficulty:'easy', topic:'Arrays', solved:false, description:`Given an array of integers nums and a target, return indices of two numbers that add up to target.\n\nExample:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]\n(nums[0] + nums[1] == 9)`, starter:{ python:`def two_sum(nums, target):\n    # Your solution here\n    pass`, java:`public int[] twoSum(int[] nums, int target) {\n    // Your solution here\n    return new int[]{};\n}` }, hint:'Use a HashMap for O(n) solution.' },
  { id:2, title:'Reverse Linked List', difficulty:'easy', topic:'Linked Lists', solved:false, description:`Reverse a singly linked list.\n\nExample:\nInput: 1 → 2 → 3 → 4 → 5\nOutput: 5 → 4 → 3 → 2 → 1`, starter:{ python:`def reverse_list(head):\n    # Your solution here\n    pass` }, hint:'Use three pointers: prev, curr, next.' },
  { id:3, title:'Valid Parentheses', difficulty:'easy', topic:'Stacks', solved:false, description:`Given a string containing only ()[]{}. Determine if the input string is valid.\n\nExample:\nInput: "()[]{}" → Output: true\nInput: "(]" → Output: false`, starter:{ python:`def is_valid(s):\n    # Your solution here\n    pass` }, hint:'Use a stack to track opening brackets.' },
  { id:4, title:'Maximum Subarray', difficulty:'medium', topic:'Dynamic Programming', solved:false, description:`Find the contiguous subarray with the largest sum.\n\nExample:\nInput: [-2,1,-3,4,-1,2,1,-5,4]\nOutput: 6 (subarray [4,-1,2,1])`, starter:{ python:`def max_subarray(nums):\n    # Kadane's Algorithm\n    pass` }, hint:"Kadane's algorithm: track current_max and global_max." },
  { id:5, title:'Binary Search', difficulty:'easy', topic:'Binary Search', solved:false, description:`Given a sorted array and target, return the index if found, else -1.\n\nExample:\nInput: nums = [-1,0,3,5,9,12], target = 9\nOutput: 4`, starter:{ python:`def search(nums, target):\n    # Binary search implementation\n    pass` }, hint:'Use left and right pointers, compare middle element.' },
  { id:6, title:'Merge Two Sorted Lists', difficulty:'easy', topic:'Linked Lists', solved:false, description:`Merge two sorted linked lists and return the merged list.\n\nExample:\nInput: 1→2→4, 1→3→4\nOutput: 1→1→2→3→4→4`, starter:{ python:`def merge_two_lists(l1, l2):\n    # Your solution here\n    pass` }, hint:'Use a dummy head node and two pointers.' },
  { id:7, title:'Climbing Stairs', difficulty:'easy', topic:'Dynamic Programming', solved:false, description:`You are climbing n stairs. Each time you can climb 1 or 2 steps. How many distinct ways can you reach the top?\n\nExample:\nn = 3 → 3 ways: (1,1,1), (1,2), (2,1)`, starter:{ python:`def climb_stairs(n):\n    # Fibonacci-like DP\n    pass` }, hint:'dp[i] = dp[i-1] + dp[i-2]' },
  { id:8, title:'Number of Islands', difficulty:'medium', topic:'Graphs', solved:false, description:`Count the number of islands in a 2D grid ('1' = land, '0' = water).\n\nExample:\nGrid:\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0\nOutput: 1`, starter:{ python:`def num_islands(grid):\n    # BFS/DFS solution\n    pass` }, hint:'Use DFS/BFS and mark visited cells.' },
];

const DIFF_COLOR = { easy:'#10b981', medium:'#f59e0b', hard:'#ef4444' };

export default function CodingPractice() {
  const [selected, setSelected] = useState(null);
  const [lang, setLang] = useState('python');
  const [code, setCode] = useState('');
  const [filter, setFilter] = useState('all');
  const [solved, setSolved] = useState({});
  const [output, setOutput] = useState(null);

  const filtered = PROBLEMS.filter(p => filter === 'all' || p.difficulty === filter);

  const openProblem = (p) => {
    setSelected(p);
    setCode(p.starter[lang] || p.starter.python || '');
    setOutput(null);
  };

  const runCode = () => {
    if (!code.trim()) return;
    setOutput({ status:'demo', message:'[Demo Mode] Code execution is simulated for the prototype.\n\nIn production, code would be sent to a secure sandbox (e.g., Judge0 API) for real evaluation.\n\nYour code has been reviewed. Mark as solved if your logic looks correct!', passed:3, total:3 });
  };

  const markSolved = () => {
    setSolved({ ...solved, [selected.id]: true });
    setOutput({ ...output, status:'passed', message:'✅ Marked as solved! Your coding stats will update.' });
  };

  const totalSolved = Object.keys(solved).length;

  return (
    <div>
      <DemoBanner message="Code execution is simulated (demo mode). In production, a secure sandbox like Judge0 would be used for real evaluation." />
      <PageHeader title="Coding Practice" subtitle="Practice DSA problems and track your progress" />

      <div style={{ display:'grid', gridTemplateColumns:'300px 1fr', gap:20 }}>
        {/* Problem list */}
        <div>
          <Card style={{ marginBottom:12, padding:12 }}>
            <div style={{ display:'flex', gap:6, flexWrap:'wrap' }}>
              {['all','easy','medium','hard'].map(f => (
                <button key={f} onClick={() => setFilter(f)}
                  style={{ padding:'5px 12px', borderRadius:20, border:'none', background:filter===f?'#4f46e5':'#f1f5f9', color:filter===f?'white':'#64748b', fontWeight:600, fontSize:11, cursor:'pointer', textTransform:'capitalize' }}>
                  {f}
                </button>
              ))}
            </div>
            <div style={{ marginTop:10, fontSize:12, color:'#64748b' }}>Solved: {totalSolved}/{PROBLEMS.length}</div>
          </Card>
          {filtered.map(p => (
            <div key={p.id} onClick={() => openProblem(p)}
              style={{ padding:'12px 16px', marginBottom:6, background:selected?.id===p.id?'#eef2ff':'white', border:`1px solid ${selected?.id===p.id?'#4f46e5':'#e2e8f0'}`, borderRadius:10, cursor:'pointer' }}>
              <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center' }}>
                <div>
                  <div style={{ display:'flex', alignItems:'center', gap:6 }}>
                    {solved[p.id] && <FiCheck size={12} color="#10b981" />}
                    <span style={{ fontWeight:600, fontSize:13 }}>{p.title}</span>
                  </div>
                  <div style={{ fontSize:11, color:'#94a3b8', marginTop:3 }}>{p.topic}</div>
                </div>
                <Badge label={p.difficulty} type={p.difficulty==='easy'?'success':p.difficulty==='medium'?'warning':'danger'} />
              </div>
            </div>
          ))}
        </div>

        {/* Editor panel */}
        {selected ? (
          <div style={{ display:'flex', flexDirection:'column', gap:16 }}>
            <Card>
              <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start', marginBottom:12 }}>
                <div>
                  <h2 style={{ fontWeight:700, fontSize:18, marginBottom:4 }}>{selected.title}</h2>
                  <div style={{ display:'flex', gap:8 }}>
                    <Badge label={selected.difficulty} type={selected.difficulty==='easy'?'success':selected.difficulty==='medium'?'warning':'danger'} />
                    <Badge label={selected.topic} type="info" />
                  </div>
                </div>
              </div>
              <pre style={{ background:'#f8fafc', padding:16, borderRadius:8, fontSize:13, lineHeight:1.8, whiteSpace:'pre-wrap', color:'#374151', fontFamily:'monospace' }}>
                {selected.description}
              </pre>
              <div style={{ marginTop:12, padding:'10px 14px', background:'#fffbeb', borderRadius:8, fontSize:12, color:'#92400e', borderLeft:'3px solid #f59e0b' }}>
                💡 Hint: {selected.hint}
              </div>
            </Card>

            <Card>
              <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:12 }}>
                <div style={{ display:'flex', gap:8 }}>
                  {['python','java'].map(l => (
                    <button key={l} onClick={() => { setLang(l); setCode(selected.starter[l]||selected.starter.python||''); }}
                      style={{ padding:'5px 14px', borderRadius:6, border:'none', background:lang===l?'#4f46e5':'#f1f5f9', color:lang===l?'white':'#64748b', fontWeight:600, fontSize:12, cursor:'pointer', textTransform:'capitalize' }}>
                      {l}
                    </button>
                  ))}
                </div>
                <div style={{ display:'flex', gap:8 }}>
                  <Btn onClick={runCode} variant="secondary" size="sm"><FiPlay /> Run</Btn>
                  <Btn onClick={markSolved} variant="success" size="sm"><FiCheck /> Mark Solved</Btn>
                </div>
              </div>
              <textarea value={code} onChange={e => setCode(e.target.value)} rows={14}
                style={{ width:'100%', padding:16, background:'#1e1b4b', color:'#a5b4fc', border:'none', borderRadius:10, fontSize:13, fontFamily:'monospace', resize:'vertical', lineHeight:1.6, outline:'none' }} />
              {output && (
                <div style={{ marginTop:12, padding:14, background:output.status==='passed'?'#f0fdf4':'#f8fafc', borderRadius:8, borderLeft:`3px solid ${output.status==='passed'?'#10b981':'#94a3b8'}` }}>
                  <pre style={{ fontSize:12, whiteSpace:'pre-wrap', color:'#374151', fontFamily:'monospace' }}>{output.message}</pre>
                </div>
              )}
            </Card>
          </div>
        ) : (
          <Card style={{ display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', minHeight:400 }}>
            <FiCode size={48} color="#e2e8f0" />
            <p style={{ color:'#94a3b8', marginTop:16, fontSize:14 }}>Select a problem to start coding</p>
          </Card>
        )}
      </div>
    </div>
  );
}
