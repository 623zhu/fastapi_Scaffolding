FROM node:22-alpine AS development

WORKDIR /app

COPY frontend/package*.json ./
RUN --mount=type=cache,target=/root/.npm npm ci

COPY frontend/ ./

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]


FROM development AS build

ARG VITE_APP_TITLE=FastAPI Vue Starter
ENV VITE_APP_TITLE=$VITE_APP_TITLE

RUN npm run build


FROM nginx:1.28-alpine AS production

COPY deploy/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
