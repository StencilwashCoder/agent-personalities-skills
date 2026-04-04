# QuickBooks MCP Server - 143+ Tools for AI Bookkeeping
# Author: Eric Grill (@EricGrill)
# Source: https://github.com/EricGrill/quickbooks-online-mcp-server
# Website: https://ericgrill.com

/**
 * QuickBooks MCP Server Implementation
 * 
 * This server provides 143+ tools for AI assistants to interact with
 * QuickBooks Online via the Model Context Protocol (MCP).
 * 
 * Features:
 * - Customer management (create, read, update, delete, search)
 * - Invoice operations (create, read, update, search, void)
 * - Chart of accounts management
 * - Vendor and bill management
 * - Employee and payroll operations
 * - Journal entries
 * - Purchase transactions
 * - Bill payments
 * 
 * Blog post: https://ericgrill.com/blog/i-needed-an-ai-bookkeeper-so-i-gave-quickbooks-143-new-tools
 */

import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { QuickbooksMCPServer } from "./server/qbo-mcp-server.js";
import { RegisterTool } from "./helpers/register-tool.js";

// Import all tools
import { CreateCustomerTool } from "./tools/create-customer.tool.js";
import { GetCustomerTool } from "./tools/get-customer.tool.js";
import { UpdateCustomerTool } from "./tools/update-customer.tool.js";
import { DeleteCustomerTool } from "./tools/delete-customer.tool.js";
import { SearchCustomersTool } from "./tools/search-customers.tool.js";

import { CreateInvoiceTool } from "./tools/create-invoice.tool.js";
import { ReadInvoiceTool } from "./tools/read-invoice.tool.js";
import { UpdateInvoiceTool } from "./tools/update-invoice.tool.js";
import { SearchInvoicesTool } from "./tools/search-invoices.tool.js";

import { CreateAccountTool } from "./tools/create-account.tool.js";
import { UpdateAccountTool } from "./tools/update-account.tool.js";
import { SearchAccountsTool } from "./tools/search-accounts.tool.js";

import { CreateVendorTool } from "./tools/create-vendor.tool.js";
import { UpdateVendorTool } from "./tools/update-vendor.tool.js";
import { DeleteVendorTool } from "./tools/delete-vendor.tool.js";
import { GetVendorTool } from "./tools/get-vendor.tool.js";
import { SearchVendorsTool } from "./tools/search-vendors.tool.js";

import { CreateBillTool } from "./tools/create-bill.tool.js";
import { UpdateBillTool } from "./tools/update-bill.tool.js";
import { DeleteBillTool } from "./tools/delete-bill.tool.js";
import { GetBillTool } from "./tools/get-bill.tool.js";
import { SearchBillsTool } from "./tools/search-bills.tool.js";

import { CreateEmployeeTool } from "./tools/create-employee.tool.js";
import { GetEmployeeTool } from "./tools/get-employee.tool.js";
import { UpdateEmployeeTool } from "./tools/update-employee.tool.js";
import { SearchEmployeesTool } from "./tools/search-employees.tool.js";

import { CreateJournalEntryTool } from "./tools/create-journal-entry.tool.js";
import { GetJournalEntryTool } from "./tools/get-journal-entry.tool.js";
import { UpdateJournalEntryTool } from "./tools/update-journal-entry.tool.js";
import { DeleteJournalEntryTool } from "./tools/delete-journal-entry.tool.js";
import { SearchJournalEntriesTool } from "./tools/search-journal-entries.tool.js";

import { CreateBillPaymentTool } from "./tools/create-bill-payment.tool.js";
import { GetBillPaymentTool } from "./tools/get-bill-payment.tool.js";
import { UpdateBillPaymentTool } from "./tools/update-bill-payment.tool.js";
import { DeleteBillPaymentTool } from "./tools/delete-bill-payment.tool.js";
import { SearchBillPaymentsTool } from "./tools/search-bill-payments.tool.js";

import { CreatePurchaseTool } from "./tools/create-purchase.tool.js";
import { GetPurchaseTool } from "./tools/get-purchase.tool.js";
import { UpdatePurchaseTool } from "./tools/update-purchase.tool.js";
import { DeletePurchaseTool } from "./tools/delete-purchase.tool.js";
import { SearchPurchasesTool } from "./tools/search-purchases.tool.js";

const main = async () => {
  const server = QuickbooksMCPServer.GetServer();

  // Register Customer Tools
  RegisterTool(server, CreateCustomerTool);
  RegisterTool(server, GetCustomerTool);
  RegisterTool(server, UpdateCustomerTool);
  RegisterTool(server, DeleteCustomerTool);
  RegisterTool(server, SearchCustomersTool);

  // Register Invoice Tools
  RegisterTool(server, CreateInvoiceTool);
  RegisterTool(server, ReadInvoiceTool);
  RegisterTool(server, UpdateInvoiceTool);
  RegisterTool(server, SearchInvoicesTool);

  // Register Account Tools
  RegisterTool(server, CreateAccountTool);
  RegisterTool(server, UpdateAccountTool);
  RegisterTool(server, SearchAccountsTool);

  // Register Vendor Tools
  RegisterTool(server, CreateVendorTool);
  RegisterTool(server, GetVendorTool);
  RegisterTool(server, UpdateVendorTool);
  RegisterTool(server, DeleteVendorTool);
  RegisterTool(server, SearchVendorsTool);

  // Register Bill Tools
  RegisterTool(server, CreateBillTool);
  RegisterTool(server, GetBillTool);
  RegisterTool(server, UpdateBillTool);
  RegisterTool(server, DeleteBillTool);
  RegisterTool(server, SearchBillsTool);

  // Register Employee Tools
  RegisterTool(server, CreateEmployeeTool);
  RegisterTool(server, GetEmployeeTool);
  RegisterTool(server, UpdateEmployeeTool);
  RegisterTool(server, SearchEmployeesTool);

  // Register Journal Entry Tools
  RegisterTool(server, CreateJournalEntryTool);
  RegisterTool(server, GetJournalEntryTool);
  RegisterTool(server, UpdateJournalEntryTool);
  RegisterTool(server, DeleteJournalEntryTool);
  RegisterTool(server, SearchJournalEntriesTool);

  // Register Bill Payment Tools
  RegisterTool(server, CreateBillPaymentTool);
  RegisterTool(server, GetBillPaymentTool);
  RegisterTool(server, UpdateBillPaymentTool);
  RegisterTool(server, DeleteBillPaymentTool);
  RegisterTool(server, SearchBillPaymentsTool);

  // Register Purchase Tools
  RegisterTool(server, CreatePurchaseTool);
  RegisterTool(server, GetPurchaseTool);
  RegisterTool(server, UpdatePurchaseTool);
  RegisterTool(server, DeletePurchaseTool);
  RegisterTool(server, SearchPurchasesTool);

  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.error("QuickBooks MCP Server running on stdio");
};

main().catch(console.error);


// ============================================================================
// Tool Registration Helper Pattern
// ============================================================================

export function RegisterTool(server: any, tool: any) {
  server.registerTool(tool.name, tool.schema, tool.handler);
}

// ============================================================================
// Example Tool Schema Pattern
// ============================================================================

export const CreateInvoiceTool = {
  name: "create_invoice",
  schema: {
    type: "object",
    properties: {
      CustomerRef: {
        type: "object",
        properties: {
          value: { type: "string", description: "Customer ID" }
        },
        required: ["value"]
      },
      Line: {
        type: "array",
        items: {
          type: "object",
          properties: {
            Amount: { type: "number" },
            DetailType: { type: "string", enum: ["SalesItemLineDetail"] },
            SalesItemLineDetail: {
              type: "object",
              properties: {
                ItemRef: {
                  type: "object",
                  properties: {
                    value: { type: "string", description: "Item ID" },
                    name: { type: "string" }
                  }
                },
                Qty: { type: "number" },
                UnitPrice: { type: "number" }
              }
            }
          }
        }
      },
      DueDate: { type: "string", format: "date" },
      PrivateNote: { type: "string" }
    },
    required: ["CustomerRef", "Line"]
  },
  handler: async (params: any) => {
    // Implementation calls QuickBooks API
    const response = await fetch("https://quickbooks.api.intuit.com/v3/company/{realmId}/invoice", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${accessToken}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(params)
    });
    return response.json();
  }
};
