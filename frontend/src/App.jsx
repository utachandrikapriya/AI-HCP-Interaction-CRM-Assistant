import React, { useState, useEffect, useRef } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { 
  User, Stethoscope, Building2, Calendar, Clock, MapPin, 
  Activity, FileText, Package, HelpCircle, AlertTriangle, 
  CheckCircle2, Send, RefreshCw, Bot, Sparkles, Smile, Meh, 
  Frown, ClipboardList, Info
} from 'lucide-react'
import { 
  setFormState, resetForm, addMessage, setLoading, 
  setApiKeysStatus, resetAll 
} from './store/store'

const BACKEND_URL = "http://localhost:8000"

export default function App() {
  const dispatch = useDispatch()
  const { formState, chatHistory, isLoading } = useSelector(state => state.crm)
  
  const [inputText, setInputText] = useState("")
  const [backendConnected, setBackendConnected] = useState(false)
  const chatEndRef = useRef(null)

  // Scroll to bottom of chat whenever messages or loading state change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatHistory, isLoading])

  // Sync form state from backend on mount
  useEffect(() => {
    fetch(`${BACKEND_URL}/api/interaction`)
      .then(res => {
        if (!res.ok) throw new Error("Backend connection failed")
        return res.json()
      })
      .then(data => {
        dispatch(setFormState(data))
        setBackendConnected(true)
      })
      .catch(err => {
        console.warn("Could not connect to backend server. Operating in Simulation Mode.")
        setBackendConnected(false)
      })
  }, [dispatch])

  // Client-side simulation fallback
  const runFrontendSimulation = (text) => {
    const textLower = text.toLowerCase()
    let toolTriggered = null
    let messageResponse = ""
    let newFormState = { ...formState }

    const now = new Date()
    const todayStr = now.toISOString().split('T')[0]
    const yesterday = new Date(now)
    yesterday.setDate(now.getDate() - 1)
    const yesterdayStr = yesterday.toISOString().split('T')[0]

    // 1. Summary
    if (textLower.includes("summary") || textLower.includes("summarize")) {
      toolTriggered = "Generate Summary"
      const hcp = formState.hcpName || "the healthcare professional"
      const org = formState.organization ? ` at ${formState.organization}` : ""
      const products = formState.productsDiscussed.join(", ") || "the product portfolio"
      const sentiment = formState.sentiment || "Neutral"
      const summaryText = `Sales representative met ${hcp}${org} to discuss ${products}. Detailing materials were shared. The overall meeting sentiment was ${sentiment} and the response was favorable.`
      newFormState.summary = summaryText
      messageResponse = `Using Generate Summary Tool...\n\nCRM Summary generated:\n\n"${summaryText}"`
    }
    // 2. Validate
    else if (textLower.includes("validate") || textLower.includes("validation")) {
      toolTriggered = "Validate Interaction"
      const missing = []
      const fields = {
        hcpName: "HCP Name",
        specialty: "Specialty",
        organization: "Organization",
        interactionType: "Interaction Type",
        interactionDate: "Interaction Date",
        interactionTime: "Interaction Time",
        location: "Location",
        duration: "Duration",
        productsDiscussed: "Products Discussed",
        topicsDiscussed: "Topics Discussed",
        materialsShared: "Materials Shared",
        samplesDistributed: "Samples Distributed",
        questionsRaised: "Questions Raised",
        objections: "Objections",
        followUpDate: "Follow-up Date",
        sentiment: "Sentiment",
        interactionOutcome: "Interaction Outcome",
        summary: "Summary"
      }
      Object.keys(fields).forEach(key => {
        const val = formState[key]
        if (Array.isArray(val)) {
          if (val.length === 0) missing.push(fields[key])
        } else if (!val || val.trim() === "") {
          missing.push(fields[key])
        }
      })
      if (missing.length === 0) {
        messageResponse = "Using Validate Interaction Tool...\n\n✅ Validation complete. All fields are successfully populated!"
      } else {
        messageResponse = `Using Validate Interaction Tool...\n\nValidation Results:\nMissing:\n${missing.map(f => `• ${f}`).join('\n')}\n\nEverything else is complete.`
      }
    }
    // 3. Suggest follow-up
    else if (textLower.includes("suggest") || textLower.includes("follow-up") || textLower.includes("next step") || textLower.includes("next action")) {
      toolTriggered = "Suggest Follow-up"
      const hcp = formState.hcpName || "Dr. Smith"
      const products = formState.productsDiscussed.join(", ") || "products discussed"
      const suggestions = [
        `Schedule follow-up meeting with ${hcp} next week.`,
        products ? `Share latest efficacy study on ${products}.` : "Send pricing brochure and clinical study papers.",
        "Add to monthly medical update distribution list."
      ]
      messageResponse = `Using Suggest Follow-up Tool...\n\nSuggested Follow-ups for ${hcp}:\n${suggestions.map(s => `• ${s}`).join('\n')}`
    }
    // 4. Edit (Modify specific fields only)
    else if (
      textLower.includes("change") || textLower.includes("edit") || 
      textLower.includes("replace") || textLower.includes("update") || 
      textLower.includes("instead of") || textLower.includes("sentiment to") || 
      textLower.includes("product to")
    ) {
      toolTriggered = "Edit Interaction"
      const editsMade = []
      
      // Sentiment edit
      if (textLower.includes("neutral")) {
        newFormState.sentiment = "Neutral"
        editsMade.push("sentiment")
      } else if (textLower.includes("positive")) {
        newFormState.sentiment = "Positive"
        editsMade.push("sentiment")
      } else if (textLower.includes("negative")) {
        newFormState.sentiment = "Negative"
        editsMade.push("sentiment")
      }

      // Product edit
      if (textLower.includes("cardiomax")) {
        newFormState.productsDiscussed = ["CardioMax"]
        editsMade.push("productsDiscussed")
      } else if (textLower.includes("oncoboost")) {
        newFormState.productsDiscussed = ["OncoBoost"]
        editsMade.push("productsDiscussed")
      } else if (textLower.includes("cardiolife")) {
        newFormState.productsDiscussed = ["CardioLife"]
        editsMade.push("productsDiscussed")
      }

      // Specialty edit
      if (textLower.includes("cardiology")) {
        newFormState.specialty = "Cardiology"
        editsMade.push("specialty")
      } else if (textLower.includes("pediatrics")) {
        newFormState.specialty = "Pediatrics"
        editsMade.push("specialty")
      }

      if (editsMade.length === 0) {
        // Default edit
        newFormState.sentiment = "Neutral"
        editsMade.push("sentiment")
      }
      messageResponse = `Using Edit Interaction Tool...\n\nModified field(s): ${editsMade.join(", ")}. Form state updated.`
    }
    // 5. Log Interaction (Extract text details)
    else {
      toolTriggered = "Log Interaction"
      
      // Extract name
      let hcpName = "Dr. John Smith"
      if (textLower.includes("dr. ")) {
        const match = text.match(/Dr\.\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?/)
        if (match) hcpName = match[0]
      } else if (textLower.includes("dr ")) {
        const match = text.match(/dr\s+[A-Za-z]+(?:\s+[A-Za-z]+)?/i)
        if (match) {
          const parts = match[0].split(/\s+/)
          hcpName = "Dr. " + parts.slice(1).map(p => p.charAt(0).toUpperCase() + p.slice(1).toLowerCase()).join(" ")
        }
      }

      // Extract date
      let date = todayStr
      if (textLower.includes("yesterday")) {
        date = yesterdayStr
      }

      // Extract products
      let products = ["CardioLife"]
      if (textLower.includes("cardiomax")) {
        products = ["CardioMax"]
      } else if (textLower.includes("oncoboost")) {
        products = ["OncoBoost"]
      }

      // Extract materials
      let materials = []
      if (textLower.includes("brochure")) {
        materials.push("Product Brochure")
      }
      if (textLower.includes("clinical paper") || textLower.includes("clinical study") || textLower.includes("study") || textLower.includes("paper")) {
        materials.push("Clinical Study Paper")
      }
      if (materials.length === 0) {
        materials.push("Detailing Slide Deck")
      }

      // Extract sentiment
      let sentiment = "Positive"
      if (textLower.includes("neutral") || textLower.includes("interested but busy")) {
        sentiment = "Neutral"
      } else if (textLower.includes("negative") || textLower.includes("not interested")) {
        sentiment = "Negative"
      }

      newFormState = {
        ...newFormState,
        hcpName,
        interactionDate: date,
        productsDiscussed: products,
        materialsShared: materials,
        sentiment,
        interactionType: "Meeting",
        organization: "General Hospital",
        specialty: "Cardiology",
        topicsDiscussed: ["Product Efficacy", "Patient Safety"],
        interactionOutcome: "Doctor showed strong interest in new clinical study data."
      }

      messageResponse = `Using Log Interaction Tool...\n\nSuccessfully logged interaction for ${hcpName}.\nCaptured products: ${products.join(", ")}, materials: ${materials.join(", ")}, sentiment: ${sentiment}.`
    }

    return { newFormState, messageResponse, toolTriggered }
  }

  const handleSend = async (textToSend) => {
    const text = textToSend || inputText
    if (!text.trim()) return

    // Add user message to chat log
    dispatch(addMessage({ role: 'user', content: text }))
    setInputText("")
    dispatch(setLoading(true))

    if (!backendConnected) {
      // Simulate client side response in 800ms
      setTimeout(() => {
        const { newFormState, messageResponse, toolTriggered } = runFrontendSimulation(text)
        dispatch(setFormState(newFormState))
        dispatch(addMessage({
          role: 'assistant',
          content: messageResponse,
          toolTriggered
        }))
        dispatch(setLoading(false))
      }, 800)
      return
    }

    // Format chat history for backend agent context
    const formattedHistory = chatHistory
      .filter(msg => !msg.content.startsWith("Hello!") && !msg.content.startsWith("Form reset"))
      .map(msg => ({
        role: msg.role,
        content: msg.content
      }))

    try {
      const response = await fetch(`${BACKEND_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: text,
          history: formattedHistory
        })
      })

      if (!response.ok) throw new Error("Server error")
      const result = await response.json()

      // Update Form State in Redux
      dispatch(setFormState(result.formState))

      // Add Assistant Message with tool log info
      dispatch(addMessage({
        role: 'assistant',
        content: result.response,
        toolTriggered: result.toolTriggered
      }))
    } catch (error) {
      console.error("Chat error:", error)
      dispatch(addMessage({
        role: 'assistant',
        content: "⚠️ Communicating with the agent server failed. Using local Simulation fallback."
      }))
      // Run local simulation
      const { newFormState, messageResponse, toolTriggered } = runFrontendSimulation(text)
      dispatch(setFormState(newFormState))
      dispatch(addMessage({
        role: 'assistant',
        content: messageResponse,
        toolTriggered
      }))
    } finally {
      dispatch(setLoading(false))
    }
  }

  const handleReset = async () => {
    if (window.confirm("Are you sure you want to clear the current interaction form?")) {
      dispatch(setLoading(true))
      if (!backendConnected) {
        setTimeout(() => {
          dispatch(resetAll())
          dispatch(setLoading(false))
        }, 500)
        return
      }

      try {
        const res = await fetch(`${BACKEND_URL}/api/reset`, { method: 'POST' })
        const data = await res.json()
        dispatch(resetAll())
        dispatch(setFormState(data))
      } catch (err) {
        console.error("Error resetting form:", err)
        dispatch(resetAll())
      } finally {
        dispatch(setLoading(false))
      }
    }
  }

  const suggestionPrompts = [
    {
      label: "📝 Log New Meeting",
      text: "Yesterday I met Dr. John Smith. We discussed CardioLife. He was very interested. I shared one brochure."
    },
    {
      label: "✏️ Modify Fields",
      text: "Change the sentiment to Neutral and replace CardioLife with CardioMax."
    },
    {
      label: "🔍 Validate Form",
      text: "Validate this interaction for missing fields."
    },
    {
      label: "📊 Summarize Log",
      text: "Generate a professional CRM summary of this meeting."
    },
    {
      label: "💡 Suggest Actions",
      text: "Suggest some next action follow-ups based on this interaction."
    }
  ]

  // Render list of chips for arrays in the form
  const renderChips = (list) => {
    if (!list || list.length === 0) {
      return <div className="chip-empty">None specified</div>
    }
    return list.map((item, idx) => (
      <span key={idx} className="chip">
        {item}
      </span>
    ))
  }

  return (
    <>
      {/* Header */}
      <header className="app-header">
        <div className="app-logo">
          <Activity className="logo-icon animate-pulse" size={24} />
          <span>HCP Interaction CRM Assistant</span>
        </div>
        <div className="flex gap-4 items-center">
          {backendConnected ? (
            <div className="api-status">
              <CheckCircle2 size={14} />
              <span>Backend Connected</span>
            </div>
          ) : (
            <div className="api-status simulated">
              <Sparkles size={14} />
              <span>Simulation Active (Offline Fallback)</span>
            </div>
          )}
        </div>
      </header>

      {/* Main Containers */}
      <div className="app-container">
        
        {/* Left Panel: Form Details (Read-only) */}
        <div className="form-panel">
          <div className="panel-title-container">
            <h2 className="panel-title">
              <ClipboardList size={20} className="color-primary" />
              Interaction Details Form
            </h2>
            <span className="ai-only-badge">AI Edit Only</span>
          </div>

          <form className="hcp-form" onSubmit={(e) => e.preventDefault()}>
            
            {/* Field 1: HCP Name */}
            <div className="form-group">
              <label>
                <User size={14} /> HCP Name
              </label>
              <input 
                type="text" 
                value={formState.hcpName || ""} 
                disabled 
                placeholder="No HCP logged" 
              />
            </div>

            {/* Field 2: Specialty */}
            <div className="form-group">
              <label>
                <Stethoscope size={14} /> Specialty
              </label>
              <input 
                type="text" 
                value={formState.specialty || ""} 
                disabled 
                placeholder="No specialty logged" 
              />
            </div>

            {/* Field 3: Organization */}
            <div className="form-group">
              <label>
                <Building2 size={14} /> Organization
              </label>
              <input 
                type="text" 
                value={formState.organization || ""} 
                disabled 
                placeholder="No organization logged" 
              />
            </div>

            {/* Field 4: Interaction Type */}
            <div className="form-group">
              <label>
                <Info size={14} /> Interaction Type
              </label>
              <input 
                type="text" 
                value={formState.interactionType || ""} 
                disabled 
                placeholder="Meeting, Call, Email, etc." 
              />
            </div>

            {/* Field 5: Interaction Date */}
            <div className="form-group">
              <label>
                <Calendar size={14} /> Interaction Date
              </label>
              <input 
                type="text" 
                value={formState.interactionDate || ""} 
                disabled 
                placeholder="YYYY-MM-DD" 
              />
            </div>

            {/* Field 6: Interaction Time */}
            <div className="form-group">
              <label>
                <Clock size={14} /> Interaction Time
              </label>
              <input 
                type="text" 
                value={formState.interactionTime || ""} 
                disabled 
                placeholder="HH:MM" 
              />
            </div>

            {/* Field 7: Location */}
            <div className="form-group">
              <label>
                <MapPin size={14} /> Location
              </label>
              <input 
                type="text" 
                value={formState.location || ""} 
                disabled 
                placeholder="Location details" 
              />
            </div>

            {/* Field 8: Duration */}
            <div className="form-group">
              <label>
                <Clock size={14} /> Duration
              </label>
              <input 
                type="text" 
                value={formState.duration || ""} 
                disabled 
                placeholder="e.g. 30 mins" 
              />
            </div>

            {/* Field 9: Products Discussed */}
            <div className="form-group span-2">
              <label>
                <Package size={14} /> Products Discussed
              </label>
              <div className="chips-container">
                {renderChips(formState.productsDiscussed)}
              </div>
            </div>

            {/* Field 10: Topics Discussed */}
            <div className="form-group span-2">
              <label>
                <FileText size={14} /> Topics Discussed
              </label>
              <div className="chips-container">
                {renderChips(formState.topicsDiscussed)}
              </div>
            </div>

            {/* Field 11: Materials Shared */}
            <div className="form-group span-2">
              <label>
                <FileText size={14} /> Materials Shared
              </label>
              <div className="chips-container">
                {renderChips(formState.materialsShared)}
              </div>
            </div>

            {/* Field 12: Samples Distributed */}
            <div className="form-group span-2">
              <label>
                <Package size={14} /> Samples Distributed
              </label>
              <div className="chips-container">
                {renderChips(formState.samplesDistributed)}
              </div>
            </div>

            {/* Field 13: Questions Raised */}
            <div className="form-group span-2">
              <label>
                <HelpCircle size={14} /> Questions Raised
              </label>
              <div className="chips-container">
                {renderChips(formState.questionsRaised)}
              </div>
            </div>

            {/* Field 14: Objections */}
            <div className="form-group span-2">
              <label>
                <AlertTriangle size={14} /> Objections
              </label>
              <div className="chips-container">
                {renderChips(formState.objections)}
              </div>
            </div>

            {/* Field 15: Follow-up Date */}
            <div className="form-group">
              <label>
                <Calendar size={14} /> Follow-up Date
              </label>
              <input 
                type="text" 
                value={formState.followUpDate || ""} 
                disabled 
                placeholder="YYYY-MM-DD" 
              />
            </div>

            {/* Field 16: Observed Sentiment */}
            <div className="form-group">
              <label>
                <Smile size={14} /> Inferred Sentiment
              </label>
              <div className="sentiment-container">
                <div className={`sentiment-badge ${formState.sentiment?.toLowerCase() === 'positive' ? 'active positive' : ''}`}>
                  <Smile size={14} /> Positive
                </div>
                <div className={`sentiment-badge ${formState.sentiment?.toLowerCase() === 'neutral' ? 'active neutral' : ''}`}>
                  <Meh size={14} /> Neutral
                </div>
                <div className={`sentiment-badge ${formState.sentiment?.toLowerCase() === 'negative' ? 'active negative' : ''}`}>
                  <Frown size={14} /> Negative
                </div>
              </div>
            </div>

            {/* Field 17: Interaction Outcome */}
            <div className="form-group span-2">
              <label>
                <CheckCircle2 size={14} /> Interaction Outcome
              </label>
              <input 
                type="text" 
                value={formState.interactionOutcome || ""} 
                disabled 
                placeholder="Log outcome of the conversation" 
              />
            </div>

            {/* Field 18: Summary */}
            <div className="form-group span-2">
              <label>
                <FileText size={14} /> CRM Executive Summary
              </label>
              <textarea 
                rows="3" 
                value={formState.summary || ""} 
                disabled 
                placeholder="Ask the AI to generate a CRM summary or describe details to construct one..."
              />
            </div>

          </form>
        </div>

        {/* Right Panel: AI Chat Interface */}
        <div className="chat-panel">
          <div className="chat-header">
            <div className="chat-header-title">
              <Bot size={18} className="color-primary" />
              <span>AI Assistant Chat</span>
            </div>
            <button className="reset-button" onClick={handleReset}>
              <RefreshCw size={12} />
              Reset Form
            </button>
          </div>

          {/* Messages list */}
          <div className="chat-messages">
            {chatHistory.map((msg, index) => (
              <div key={index} className={`chat-bubble ${msg.role}`}>
                {msg.toolTriggered && (
                  <div className="tool-tag">
                    <Sparkles size={11} />
                    <span>Using tool: {msg.toolTriggered}</span>
                  </div>
                )}
                <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
              </div>
            ))}
            
            {isLoading && (
              <div className="agent-thinking">
                <Bot size={14} className="color-primary animate-pulse" />
                <span style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>AI Syncing details...</span>
                <div className="dot-pulse">
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <div className="dot"></div>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Console inputs */}
          <div className="chat-input-container">
            {/* suggestions */}
            <div className="suggestions-grid">
              {suggestionPrompts.map((prompt, idx) => (
                <div 
                  key={idx} 
                  className="suggestion-pill"
                  onClick={() => {
                    setInputText(prompt.text)
                  }}
                >
                  {prompt.label}
                </div>
              ))}
            </div>

            <form 
              className="chat-input-form" 
              onSubmit={(e) => {
                e.preventDefault()
                handleSend()
              }}
            >
              <input 
                type="text" 
                className="chat-input" 
                placeholder="Instruct assistant to log/modify details..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                disabled={isLoading}
              />
              <button 
                type="submit" 
                className="send-button"
                disabled={isLoading || !inputText.trim()}
              >
                <Send size={16} />
              </button>
            </form>
          </div>
        </div>

      </div>
    </>
  )
}
