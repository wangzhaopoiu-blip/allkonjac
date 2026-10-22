export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.protocol === "http:") {
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    const response = await env.ASSETS.fetch(request);
    if (/^\/assets\/documents\/quotation-example-(en|th|id)\.pdf$/.test(url.pathname)) {
      const headers = new Headers(response.headers);
      headers.set("X-Robots-Tag", "noindex");
      return new Response(response.body, {status: response.status, statusText: response.statusText, headers});
    }
    return response;
  },
};
