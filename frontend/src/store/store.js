import { configureStore, createSlice } from '@reduxjs/toolkit'

const initialFormState = {
  hcpName: "",
  specialty: "",
  organization: "",
  interactionType: "",
  interactionDate: "",
  interactionTime: "",
  location: "",
  duration: "",
  productsDiscussed: [],
  topicsDiscussed: [],
  materialsShared: [],
  samplesDistributed: [],
  questionsRaised: [],
  objections: [],
  followUpDate: "",
  sentiment: "",
  interactionOutcome: "",
  summary: ""
}

const crmSlice = createSlice({
  name: 'crm',
  initialState: {
    formState: initialFormState,
    chatHistory: [
      {
        role: "assistant",
        content: "Hello! I am your AI CRM Assistant. You can describe your HCP interaction in natural language, and I will update the form details for you. Try typing:\n\n'Yesterday I met Dr. John Smith to discuss CardioLife.'"
      }
    ],
    isLoading: false,
    hasRealApiKeys: false
  },
  reducers: {
    setFormState: (state, action) => {
      state.formState = { ...state.formState, ...action.payload }
    },
    resetForm: (state) => {
      state.formState = initialFormState
    },
    addMessage: (state, action) => {
      state.chatHistory.push(action.payload)
    },
    setLoading: (state, action) => {
      state.isLoading = action.payload
    },
    setApiKeysStatus: (state, action) => {
      state.hasRealApiKeys = action.payload
    },
    resetAll: (state) => {
      state.formState = initialFormState
      state.chatHistory = [
        {
          role: "assistant",
          content: "Form reset completed. How can I assist you with your next HCP interaction log?"
        }
      ]
      state.isLoading = false
    }
  }
})

export const { setFormState, resetForm, addMessage, setLoading, setApiKeysStatus, resetAll } = crmSlice.actions

export const store = configureStore({
  reducer: {
    crm: crmSlice.reducer
  }
})
