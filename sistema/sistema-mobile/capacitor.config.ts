import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'io.ionic.starter',
  appName: 'sistema-mobile',
  webDir: 'www',
  
  server: {
    url: 'http://localhost:8000',
    cleartext: true
  }
};

export default config;
