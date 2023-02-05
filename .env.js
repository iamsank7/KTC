const production = {
    ...process.env,
    NODE_ENV: process.env.NODE_ENV || 'production',
};

const development = {
    ...process.env,
    NODE_ENV: process.env.NODE_ENV || 'development',
    PORT: '9000',
    Meta_WA_accessToken:'EAAWNXwCMvnYBAIln4LgWnjtlTIPv9ZCRvUDYEZBoDRnaPVWvEUW0fCZAWMQaR6p15d7GqOjPeBSZBrD8hBwPo52mzysq2V0M9yqWNYFK0pJ4D9MRuc2ZCEsZAb3tlZAUOPNMyNZBA0aFlSKrqtHCKNptPQTLu33rZA7FZBOj3gu1kHnJW2OG1trZBRZBUcBVyxjctJzhckfRZA3VMywZDZD',
    Meta_WA_SenderPhoneNumberId: '116564778008868',
    Meta_WA_wabaId: '102156982799378',
    Meta_WA_VerifyToken: '678c7f25-549c-4e6a-8fcc-1f58c024425e',
};

const fallback = {
    ...process.env,
    NODE_ENV: undefined,
};

module.exports = (environment) => {
    console.log(`Execution environment selected is: "${environment}"`);
    if (environment === 'production') {
        return production;
    } else if (environment === 'development') {
        return development;
    } else {
        return fallback;
    }
};