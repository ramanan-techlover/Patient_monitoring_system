import create from 'zustand';
import { setupAlertListener } from '../services/alertService';

const useMonitoringStore = create((set, get) => ({
  // Pain Monitoring State
  currentPainScore: 0,
  painStatus: 'COMFORT',
  painHistory: [],
  painAlert: null,

  // Agitation Monitoring State
  currentAgitationLevel: 0,
  agitationStatus: 'CALM',
  agitationHistory: [],
  agitationAlert: null,

  // Audio Monitoring State
  currentAudioTranscript: '',
  detectedKeywords: [],
  audioHistory: [],
  audioAlert: null,

  // General Alert State
  allAlerts: [],
  criticalAlerts: [],
  isListening: false,

  // Actions
  setPainData: (data) => set((state) => ({
    currentPainScore: data?.score ?? 0,
    painStatus: data?.status ?? 'COMFORT',
    painHistory: [...state.painHistory, { timestamp: new Date(), ...data }].slice(-100),
    painAlert: data?.status === 'PAIN DETECTED' ? data : null,
  })),

  setAgitationData: (data) => set((state) => ({
    currentAgitationLevel: data?.level ?? 0,
    agitationStatus: data?.status ?? 'CALM',
    agitationHistory: [...state.agitationHistory, { timestamp: new Date(), ...data }].slice(-100),
    agitationAlert: data?.status !== 'CALM' ? data : null,
  })),

  setAudioData: (data) => set((state) => ({
    currentAudioTranscript: data?.text ?? '',
    detectedKeywords: data?.keywords || [],
    audioHistory: [...state.audioHistory, { timestamp: new Date(), ...data }].slice(-100),
    audioAlert: data?.keywords && data.keywords.length > 0 ? data : null,
  })),

  addAlert: (alert) => set((state) => ({
    allAlerts: [alert, ...state.allAlerts].slice(-50),
    criticalAlerts: alert.severity === 'CRITICAL' 
      ? [alert, ...state.criticalAlerts].slice(-20)
      : state.criticalAlerts,
  })),

  clearAlerts: () => set({
    painAlert: null,
    agitationAlert: null,
    audioAlert: null,
  }),

  initializeAlertSystem: () => {
    set({ isListening: true });
    setupAlertListener((alert) => {
      get().addAlert(alert);
      
      // Route to appropriate handler based on type
      if (alert.type === 'PAIN') {
        get().setPainData(alert.data);
      } else if (alert.type === 'AGITATION') {
        get().setAgitationData(alert.data);
      } else if (alert.type === 'AUDIO') {
        get().setAudioData(alert.data);
      }
    });
  },
}));

export default useMonitoringStore;
